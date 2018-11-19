#!/usr/bin/python
# coding: utf-8
# Written by: Mike Cao <mike.cao@oracle.com>
# Version 1.0 - 04-Nov-2018
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


def get_compartments(identity, tenancy_id):
    '''
    Retrieve the list of compartments under the tenancy.
    '''
    compartment_ocids = []
    #  Store tenancy id as the first compartment
    # compartment_ocids.append(tenancy_id)
    list_compartments_response = oci.pagination.list_call_get_all_results(
        identity.list_compartments,
        compartment_id=tenancy_id,
        compartment_id_in_subtree=True).data
    for c in list_compartments_response:
        ##compartment_ocids.append(c.id)
        if c.lifecycle_state == "ACTIVE":
            compartment_ocids.append(c)
    return compartment_ocids

##https://community.oracle.com/thread/4119240 
###We might merge https://github.com/AnykeyNL/OCI-Python/blob/master/shapes.py in the future.
def get_mem_by_shape(shape_name):
   # GB
    mem_list = {'VM.Standard1.1':7,
            'VM.Standard2.1':15,
            'VM.Standard2.2':30,
            'VM.Standard1.2':14,
            'VM.Standard1.4':28}
    return mem_list[shape_name]

def get_cpu_by_shape(shape_name):
    cpu_list = {'VM.Standard1.1':1,
            'VM.Standard2.1':1,
            'VM.Standard2.2':2,
            'VM.Standard1.2':2,
            'VM.Standard1.4':4}
    return cpu_list[shape_name]


def get_all_shapes(compute_client, compartment_ocids):

    for c in compartment_ocids:
        list_shapes = compute_client.list_shapes(c)
        data = list_shapes.data
        while list_shapes.has_next_page:
            list_shapes = compute_client(c, page=list_shapes.next_page)
            data.extend(list_shapes.data)
        if len(data)!=0:
            print type(data[0])
        #print data
        #return data
class monitor_instance_per_c:
    def __init__(self):
        self.instances_count = 0
        self.running_instances_count = 0
        self.instances_cpu = 0
        self.instances_mem = 0
        self.running_instances_cpu = 0
        self.running_instances_mem = 0
        self.oc = oci.identity.models.Compartment()

def volume_handling(data, volume_handle):
    #reuse monitor_instance_per_c class, so pls ignore the strange name
    volume_handle.instances_count = len(data) #volume count:
    for i in range(len(data)):
        ## According to https://oracle-cloud-infrastructure-python-sdk.readthedocs.io/en/latest/api/core/models/oci.core.models.Instance.html?highlight=oci%20core%20models%20instance%20instance
        ## Allowed values for this property are: "PROVISIONING", "RESTORING", "AVAILABLE", "TERMINATING", "TERMINATED", "FAULTY", 'UNKNOWN_ENUM_VALUE'. Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        if data[i].lifecycle_state != 'TERMINATED' and data[i].lifecycle_state!= 'TERMINATING':
            volume_size = data[i].size_in_gbs
            volume_handle.instances_mem += volume_size #use instance_mem to manage instance_volume
    return(volume_handle)

def get_all_volumes(volume, compartment_ocids):
    '''
    volume audit report'.
    '''
    volume_summary_report = []
    for c_object in compartment_ocids:
        c = c_object.id
        #c='ocid1.compartment.oc1..aaaaaaaa3hg6hurigmr4bdbngby6dcjiug24f2s4p5zpqw3akafe7in5cxua'
        get_volumes = volume.list_volumes(c)
        data = get_volumes.data
        while get_volumes.has_next_page:
            get_volumes = volume.list_volumes(c, page=list_computes.next_page)
            data.extend(get_volumes.data)

        volume_monitor_summary = monitor_instance_per_c()
        volume_monitor_summary.oc = c_object
        if len(data) != 0:
            volume_monitor_summary = volume_handling(data, volume_monitor_summary)
        volume_summary_report.append(volume_monitor_summary)
    volume_monitor_summary_all = monitor_instance_per_c()
    content = "================Volume Summry Report Per Comparment=======================\n"
    for i in range(len(volume_summary_report)):
        volume_monitor_summary_all.instances_count += volume_summary_report[i].instances_count
        volume_monitor_summary_all.instances_mem += volume_summary_report[i].instances_mem
        content += "*Compartment_name \t\t%s\n" % (volume_summary_report[i].oc.name)
        content += "*Compartment DESC \t\t%s\n" % (volume_summary_report[i].oc.description)
        content += "*Total volume count\t\t%d\n" % (volume_summary_report[i].instances_count)
        content += "*Total Volume Size:\t\t%dGB\n\n" % (volume_summary_report[i].instances_mem)
  
    content += "================Volume Summry Report in total=======================\n"
    content += "*Total volume count\t\t%d\n" % (volume_monitor_summary_all.instances_count)
    content += "*Total Volume Size\t\t%dGB\n" % (volume_monitor_summary_all.instances_mem)


        #  Results for a compartment 'c' for a region defined
        #  in 'audit' object.
    return content


def instance_handling(data, instance_handle):
    instance_handle.instances_count = 0
    for i in range(len(data)):
        if (data[i].lifecycle_state != "TERMINATED" and data[i].lifecycle_state != "TERMINATING"):
            instance_cpu = get_cpu_by_shape(data[i].shape)
            instance_mem = get_mem_by_shape(data[i].shape)
            instance_handle.instances_cpu += instance_cpu
            instance_handle.instances_mem += instance_mem
            instance_handle.instances_count += 1
        ## According to https://oracle-cloud-infrastructure-python-sdk.readthedocs.io/en/latest/api/core/models/oci.core.models.Instance.html?highlight=oci%20core%20models%20instance%20instance 
        ##Allowed values for this property are: "PROVISIONING", "RUNNING", "STARTING", "STOPPING", "STOPPED", "CREATING_IMAGE", "TERMINATING", "TERMINATED", 'UNKNOWN_ENUM_VALUE'. Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
            if data[i].lifecycle_state != "STOPPED":
                instance_handle.running_instances_cpu += instance_cpu
                instance_handle.running_instances_mem += instance_mem
                instance_handle.running_instances_count += 1

    return(instance_handle)

def send_report_out(subject, content):
    email_client = email_notification.Email()
    email_client.send_mail(subject, content)

def get_all_instances(compute, compartment_ocids):
    '''
    Get events iteratively for each compartment defined in 'compartments_ocids'
    for the region defined in 'compute'.
    '''
    instance_summary_report = []

    for c_object in compartment_ocids:
        c = c_object.id
        list_computes = compute.list_instances(c)

        data = list_computes.data
        while list_computes.has_next_page:
            list_computes = compute.list_instances(c, page=list_computes.next_page)
            data.extend(list_computes.data)

        instance_monitor_summary = monitor_instance_per_c()
        instance_monitor_summary.oc = c_object
        if len(data) != 0:
            instance_monitor_summary = instance_handling(data, instance_monitor_summary)
        instance_summary_report.append(instance_monitor_summary)
    instance_monitor_summary_all = monitor_instance_per_c()
    content = ""
    content += "================Instance Summry Report Per Comparment========================\n"
    for i in range(len(instance_summary_report)):
        instance_monitor_summary_all.instances_count += instance_summary_report[i].instances_count
        instance_monitor_summary_all.instances_cpu += instance_summary_report[i].instances_cpu
        instance_monitor_summary_all.instances_mem += instance_summary_report[i].instances_mem
        instance_monitor_summary_all.running_instances_count += instance_summary_report[i].running_instances_count
        instance_monitor_summary_all.running_instances_cpu += instance_summary_report[i].running_instances_cpu
        instance_monitor_summary_all.running_instances_mem += instance_summary_report[i].running_instances_mem
        
        ##print results
        if instance_summary_report[i].running_instances_count !=0:
            content += "*Compartment_name \t\t%s\n" % (instance_summary_report[i].oc.name)
            content += "*Compartment DESC \t\t%s\n" % (instance_summary_report[i].oc.description)
            content += "*Total instances count:\t\t%d\n" % (instance_summary_report[i].instances_count)
            content += "*Running instances count:\t%d\n" % (instance_summary_report[i].running_instances_count)
            content += "*Total instances CPU count:\t%d\n" % (instance_summary_report[i].instances_cpu)
            content += "*Total instances mem count:\t%d\n" % (instance_summary_report[i].instances_mem)
            content += "*Running instances CPU count:\t%d\n" % (instance_summary_report[i].running_instances_cpu)
            content += "*Running instances mem count:\t%d GB \n\n" % (instance_summary_report[i].running_instances_mem)
        else:
            content += "*Compartment %s:\t 0|%d instances running\n\n" % (instance_summary_report[i].oc.name, instance_summary_report[i].instances_count)
        content += "**************************************************************************\n"

    
    content += "================Instance Summry Report All =================================\n"
    content += "*Total instances count:\t%d\n" % (instance_monitor_summary_all.instances_count)
    content += "*Total instances CPU count:\t%d\n" % (instance_monitor_summary_all.instances_cpu)
    content += "*Total instances mem count:\t%d\n" % (instance_monitor_summary_all.instances_mem)
    content += "*Running instances count:\t%d\n"% (instance_monitor_summary_all.running_instances_count)
    content += "*Running instances CPU count:\t%d\n" % (instance_monitor_summary_all.running_instances_cpu)
    content += "*Running instances mem count:\t%d GB\n" % (instance_monitor_summary_all.running_instances_mem)
    return content

def get_all_db_system(dbs, compartment_ocids):
    list_of_db_systems = []
    for c_object in compartment_ocids:
        c = c_object.id
        db_lists = oci.pagination.list_call_get_all_results(
            dbs.list_db_systems,
            compartment_id=c).data
        list_of_db_systems.extend(db_lists)
    content = ""
    count = 0
    size = 0
    cpu = 0
    special_monitoring = ""
    content += "================DB Summry Report Per Comparment========================\n"
    for i in list_of_db_systems:
        if i.lifecycle_state == "AVAILABLE" or i.lifecycle_state == "PROVISIONING":
            count += 1
            size += i.data_storage_size_in_gbs
            cpu += get_cpu_by_shape(i.shape)
            if i.database_edition != "STANDARD_EDITION":
                special_monitoring += "DB %s are using %s DB\n" %(i.display_name,i.database_edition)
    content += "*Total DB count is %d \n" %(count)
    content += "*Total DB cpu is %d \n" %(cpu)
    content += "*Total DB extra storage size is %d \n" % (size)
    content += special_monitoring

        
            
    
#    content = instance_handling(list_of_db_systems)
    return content



#  Setting configuration
#  Default path for configuration file is "~/.oci/config"
#config = oci.config.from_file()
if len(sys.argv) == 1:
    config = oci.config.from_file(file_location='~/.oci/config', profile_name = "DEFAULT")
    tenancy_name = "default"
elif len(sys.argv) == 2:
    config = oci.config.from_file(file_location='~/.oci/config', profile_name = sys.argv[1])
    tenancy_name = sys.argv[1]
else:
    print 'print error found'
    sys.exit(1)

tenancy_id = config["tenancy"]

#  Initiate the client with the locally available config.
identity = oci.identity.IdentityClient(config)

# This array will be used to store the list of available regions.
regions = get_regions(identity)

# This array will be used to store the list of compartments in the tenancy.
compartments = get_compartments(identity, tenancy_id)


compute_client = oci.core.ComputeClient(config)
shape = oci.core.models.Shape()
block_storage_client = oci.core.BlockstorageClient(config)
db_client = oci.database.DatabaseClient(config)

#  For each region get the logs for each compartment.
compute_client.base_client.set_region('us-ashburn-1')
instance_content = get_all_instances(compute_client, compartments)
#send_report_out("Compute Audit Report -"+datetime.datetime.utcnow().strftime("%Y-%m-%d-%H:%M"),content)
#print get_all_shapes(compute_client,compartments)
volume_content = get_all_volumes(block_storage_client, compartments)
#send_report_out("Block Audit Report -"+datetime.datetime.utcnow().strftime("%Y-%m-%d-%H:%M"),content)
db_client.base_client.set_region('us-ashburn-1')
db_content = get_all_db_system(db_client,compartments)
content = instance_content + volume_content + db_content
send_report_out("tenancy - " + tenancy_name + "-"+datetime.datetime.utcnow().strftime("%Y-%m-%d-%H:%M"),content)
