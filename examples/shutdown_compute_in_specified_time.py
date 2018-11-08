#!/usr/bin/python
# coding: utf-8
# Written by: Mike Cao <mike.cao@oracle.com>
# Version 1.0 - 08-Nov-2018
import datetime
import oci
import email_notification

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
def get_compartments(identity, tenancy_id, compartment_ocids,name):
    '''
    Retrieve the list of compartments under the tenancy.
    '''

    # compartment_ocids.append(tenancy_id)
    list_compartments_response = oci.pagination.list_call_get_all_results(
        identity.list_compartments,
        compartment_id=tenancy_id).data
    for c in list_compartments_response:
        if c.lifecycle_state == "ACTIVE":
            print c.name
            compartment_ocids.append(c)
            get_compartments(identity, c.id, compartment_ocids,c.name)
    return compartment_ocids


def send_report_out(subject, content):
    email_client = email_notification.Email()
    email_client.send_mail(subject, content)

def stop_all_instances(compute, compartment_ocids):
    '''
    Get events iteratively for each compartment defined in 'compartments_ocids'
    for the region defined in 'compute'.
    '''
    data = ""

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
                instance = compute.instance_action(data[i].id, "STOP").data # this will return instance Class
                oci.wait_until(compute,compute_client.get_instance(instance.id),'lifecycle_state','STOPPED',succeed_on_not_found=True)
                print instance.display_name + "is stopped"
                data += "%s is stopped by agent as it should be up now" % instance.display_name
                
    return data

def is_apac():
    current_hour = datetime.datetime.utcnow().hour
    if current_hour >=0 and current_hour <= 13:
        return True
    else:
        return False

def is_emea():
    current_hour = datetime.datetime.utcnow().hour
    if current_hour >=8 and current_hour <= 17:
        return True
    else: 
        return False

def is_amer():
    current_hour = datetime.datetime.utcnow().hour
    if (current_hour >=0 and current_hour <= 1) or (current_hour >= 16 and current_hour < 24):
        return True
    else:
        return False


#  Setting configuration
#  Default path for configuration file is "~/.oci/config"
config = oci.config.from_file(file_location='~/.oci/config', profile_name = "DEFAULT")
tenancy_id = config["tenancy"]


#  Initiate the client with the locally available config.
identity = oci.identity.IdentityClient(config)
# This array will be used to store the list of available regions.
#regions = get_regions(identity)

compute_client = oci.core.ComputeClient(config)

#  For each region get the logs for each compartment.
compute_client.base_client.set_region('us-ashburn-1')

if not is_apac():
    print "apac VM shutdown ..."
    root_compartment_id = config["apac_root_compartment"]
    compartments_list = []
    compartments_list.append(identity.get_compartment(root_compartment_id).data)
    compartments = get_compartments(identity, root_compartment_id, compartments_list,"apac")
    status = stop_all_instances(compute_client, compartments)
    print status
    

if not is_emea():
    print "emea vm shutdown..."
    root_compartment_id = config["emea_root_compartment"]
    compartments_list = []
    compartments_list.append(identity.get_compartment(root_compartment_id).data)
    compartments = get_compartments(identity, root_compartment_id, compartments_list,"emea")
    status = stop_all_instances(compute_client, compartments)
    print status

if not is_amer():
    print "amer vm shutdown..."
    root_compartment_id = config["amer_root_compartment"]
    compartments_list = []
    compartments_list.append(identity.get_compartment(root_compartment_id).data)
    compartments = get_compartments(identity, root_compartment_id, compartments_list,"amer")
    status = stop_all_instances(compute_client, compartments)
    print status






