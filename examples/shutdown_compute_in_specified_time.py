#!/usr/bin/python
# coding: utf-8
# Written by: Mike Cao <mike.cao@oracle.com>
# Version 1.0 - 08-Nov-2018
import datetime
import oci
import email_notification
import sys

def get_regions(identity):
    '''
    To retrieve the list of all available regions.
    '''
    list_of_regions = []
    list_regions_response = identity.list_regions()
    for r in list_regions_response.data:
        list_of_regions.append(r.name)
    return list_of_regions

## Good thing is we support hirachy mode so code need to be changed.and we only check the status of 
def get_compartments(identity, tenancy_id, compartment_ocids, name):
    '''
    Retrieve the list of compartments under the tenancy.
    '''

    # compartment_ocids.append(tenancy_id)
    list_compartments_response = oci.pagination.list_call_get_all_results(
        identity.list_compartments,
        compartment_id=tenancy_id).data
    for c in list_compartments_response:
        if c.lifecycle_state == "ACTIVE":
            compartment_ocids.append(c)
            get_compartments(identity, c.id, compartment_ocids,c.name)
    return compartment_ocids


def send_report_out(subject, content):
    email_client = email_notification.Email()
    email_client.send_mail(subject, content)

def stop_all_DB(DBClient, compartment_ocids):
    data = ""
    shutdown_list = []
    for c_object in compartment_ocids:
        c = c_object.id
        DB_instances = DBClient.list_db_systems(c)

        data = DB_instances.data
        while DB_instances.has_next_page:
            DB_instances = DBClient.list_db_systems(c, page=DB_instances.next_page)
            data.extend(DB_instances.data)
        #data is the list if the computes.
        for i in range(len(data)):
            if data[i].lifecycle_state == "AVAILABLE" or data[i].lifecycle_state == "PROVISIONING":
                shutdown_list.append(data[i].display_name)
                #instance = DBClient.db_node_action(data[i].id, "STOP").data # this will return instance Class
                instance = DBClient.terminate_db_system(data[i].id)
                oci.wait_until(DBClient,DBClient.get_db_system(data[i].id),'lifecycle_state','TERMINATED',succeed_on_not_found=True)
                #print instance.display_name + "is stopped"
                #reply += "%s is stopped by agent as it should be up now" % instance.display_name

    return shutdown_list

def stop_all_instances(compute, compartment_ocids):
    '''
    Get events iteratively for each compartment defined in 'compartments_ocids'
    for the region defined in 'compute'.
    '''
    data = ""
    shutdown_list = []

    for c_object in compartment_ocids:
        c = c_object.id
        compute_instances = compute.list_instances(c)

        data = compute_instances.data
        while compute_instances.has_next_page:
            compute_instances = compute.list_instances(c, page=compute_instances.next_page)
            data.extend(compute_instances.data)
 
        #data is the list if the computes.
        for i in range(len(data)):
            if data[i].lifecycle_state == "RUNNING":
                shutdown_list.append(data[i].display_name)
                instance = compute.instance_action(data[i].id, "STOP").data # this will return instance Class
                oci.wait_until(compute,compute_client.get_instance(instance.id),'lifecycle_state','STOPPED',succeed_on_not_found=True)
                #print instance.display_name + "is stopped"
                #reply += "%s is stopped by agent as it should be up now" % instance.display_name
            
    return shutdown_list


def get_compartments_including_root(identity, root_id):
    compartments_list = []
    compartments_list.append(identity.get_compartment(root_id).data)
    return get_compartments(identity, root_id, compartments_list, "root_included")


#  Setting configuration
#  Default path for configuration file is "~/.oci/config"
if len(sys.argv) == 1:
    config = oci.config.from_file(file_location='~/.oci/config', profile_name = "DEFAULT")
elif len(sys.argv) == 2:
    config = oci.config.from_file(file_location='~/.oci/config', profile_name = sys.argv[1])
else:
    print 'print error found'
    sys.exit(1)
tenancy_id = config["tenancy"]


#  Initiate the client with the locally available config.
identity = oci.identity.IdentityClient(config)
# This array will be used to store the list of available regions.
#regions = get_regions(identity)

compute_client = oci.core.ComputeClient(config)
shutdown_list = 0
# time
current_time = datetime.datetime.utcnow()
current_hour = current_time.hour
DB_client = oci.database.DatabaseClient(config)

#  For each region get the logs for each compartment.
compute_client.base_client.set_region('us-ashburn-1')
output = "Following VMs are still in running status outside working hours!\n"
apac_shift_hours = eval(config["apac_shift_hours"])
emea_shift_hours = eval(config["emea_shift_hours"])
amer_shift_hours = eval(config["amer_shift_hours"])
#print type(amer_shift_hours)
#print amer_shift_hours
#print not 22 in amer_shift_hours
whole_compartments_list = get_compartments_including_root(identity, tenancy_id)
# this code is special for monitring units
try:
    special_compartments_root_id = config["special_compartment"]
    special_compartments_list = get_compartments_including_root(identity, special_compartments_root_id)

except:
    special_compartments_list = []

apac_compartment_id = config["apac_root_compartment"]
apac_compartments = get_compartments_including_root(identity, apac_compartment_id)
emea_compartment_id = config["emea_root_compartment"]
emea_compartments = get_compartments_including_root(identity, emea_compartment_id)
amer_compartment_id = config["amer_root_compartment"]
amer_compartments = get_compartments_including_root(identity, amer_compartment_id)

#unexpected_compartments = set(whole_compartments_list) - set(special_compartments_list) - set(apac_compartments) - set(amer_compartment_id) - set(emea_compartment_id)
unexpected_compartments = whole_compartments_list
for i in apac_compartments:
    unexpected_compartments.remove(i)
for i in emea_compartments:
    unexpected_compartments.remove(i)
for i in amer_compartments:
    unexpected_compartments.remove(i)
for i in special_compartments_list:
    unexpected_compartments.remove(i) 

if not current_hour in apac_shift_hours:
    status = stop_all_instances(compute_client, apac_compartments)
    status.extend(stop_all_DB(DB_client, apac_compartments))
    if len(status) != 0:
        shutdown_list += len(status)
        for i in range(len(status)):
            output += "APAC \t\t\t %s\n" % (status[i])
    

#if not is_emea(current_time):
if not current_hour in emea_shift_hours:
    status = stop_all_instances(compute_client, emea_compartments)
    status.extend(stop_all_DB(DB_client, emea_compartments))

    if len(status) != 0:
        shutdown_list += len(status)
        for i in range(len(status)):
            output += "EMEA \t\t\t %s\n" % (status[i])


#if not is_amer(current_time):
if not current_hour in amer_shift_hours:
    status = stop_all_instances(compute_client, amer_compartments)
    status.extend(stop_all_DB(DB_client, amer_compartments))
    if len(status) != 0:
        shutdown_list += len(status)
        for i in range(len(status)):
            output += "AMER \t\t\t %s\n" % (status[i])

#stopped all VMs in unexpected compartment
status = stop_all_instances(compute_client, unexpected_compartments)
status.extend(stop_all_DB(DB_client, unexpected_compartments))
if len(status) != 0:
    shutdown_list += len(status)
    for i in status:
        output += "Unexpected compartment\t\t\t %s\n" % (i)


if shutdown_list !=0:
    print output
    send_report_out("Compute shutdown Report - "+ current_time.strftime("%Y-%m-%d-%H:%M"),output)

