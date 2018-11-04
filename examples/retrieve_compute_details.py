#!/usr/bin/python
# coding: utf-8
# Written by: Mike Cao <mike.cao@oracle.com>
# Version 1.0 - 04-Nov-2018
import datetime
import oci


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
        compartment_id=tenancy_id).data
    for c in list_compartments_response:
        ##compartment_ocids.append(c.id)
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
        print data
        return data

def get_all_volumes(volume, compartment_ocids):
    '''
    Get events iteratively for each compartment defined in 'compartments_ocids'
    for the region defined in 'compute'.
    '''
    for c in compartment_ocids.id:
        #c='ocid1.compartment.oc1..aaaaaaaa3hg6hurigmr4bdbngby6dcjiug24f2s4p5zpqw3akafe7in5cxua'
        get_volumes = volume.list_volumes(c)
        data = get_volumes.data
        while get_volumes.has_next_page:
            get_volumes = volume.list_volumes(c, page=list_computes.next_page)
            data.extend(list_volumes.data)
        print c
        print type(c)
        print type(data)
        print data

        #  Results for a compartment 'c' for a region defined
        #  in 'audit' object.
    return data

class monitor_instance_per_c:
    def __init__(self):
        self.instances_count = 0
        self.running_instances_count = 0
        self.instances_cpu = 0
        self.instances_mem = 0
        self.running_instances_cpu = 0
        self.running_instances_mem = 0
        self.oc = oci.identity.models.Compartment()


def instance_handling(data, instance_handle):
    instance_handle.instances_count = len(data)
    for i in range(len(data)):
        instance_cpu = get_cpu_by_shape(data[i].shape)
        instance_mem = get_mem_by_shape(data[i].shape)
        instance_handle.instances_cpu += instance_cpu
        instance_handle.instances_mem += instance_mem
        ## According to https://oracle-cloud-infrastructure-python-sdk.readthedocs.io/en/latest/api/core/models/oci.core.models.Instance.html?highlight=oci%20core%20models%20instance%20instance 
        ##Allowed values for this property are: "PROVISIONING", "RUNNING", "STARTING", "STOPPING", "STOPPED", "CREATING_IMAGE", "TERMINATING", "TERMINATED", 'UNKNOWN_ENUM_VALUE'. Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        if data[i].lifecycle_state != "STOPPED":
            instance_handle.running_instances_cpu += instance_cpu
            instance_handle.running_instances_mem += instance_mem
            instance_handle.running_instances_count += 1

    return(instance_handle)
            

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
        #print type(c)
        #print type(data)

        instance_monitor_summary = monitor_instance_per_c()
        instance_monitor_summary.oc = c_object
        if len(data) != 0:
            instance_monitor_summary = instance_handling(data, instance_monitor_summary)
        instance_summary_report.append(instance_monitor_summary)
    instance_monitor_summary_all = monitor_instance_per_c()
    print "================Instance Summry Report Per Comparment========================"
    for i in range(len(instance_summary_report)):
        instance_monitor_summary_all.instances_count += instance_summary_report[i].instances_count
        instance_monitor_summary_all.instances_cpu += instance_summary_report[i].instances_cpu
        instance_monitor_summary_all.instances_mem += instance_summary_report[i].instances_mem
        instance_monitor_summary_all.running_instances_count += instance_summary_report[i].running_instances_count
        instance_monitor_summary_all.running_instances_cpu += instance_summary_report[i].running_instances_cpu
        instance_monitor_summary_all.running_instances_mem += instance_summary_report[i].running_instances_mem
        
        ##print results


        if instance_summary_report[i].running_instances_count !=0:
            print "***Compartment_name \t\t%s" % (instance_summary_report[i].oc.name)
            print "***Compartment DESC \t\t%s" % (instance_summary_report[i].oc.description)
            print "***Total instances count:\t%d" % (instance_summary_report[i].instances_count)
            print "***Running instances count:\t%d" % (instance_summary_report[i].running_instances_count)
            print "***Total instances CPU count:\t%d" % (instance_summary_report[i].instances_cpu)
            print "***Total instances mem count:\t%d " % (instance_summary_report[i].instances_mem)
            print "***Running instances CPU count:\t%d " % (instance_summary_report[i].running_instances_cpu)
            print "***Running instances mem count:\t%d GB " % (instance_summary_report[i].running_instances_mem)
        else:
            print "***Compartment %s:\t 0|%d instances running" % (instance_summary_report[i].oc.name, instance_summary_report[i].instances_count)
        print "**************************************************************************"

    
    print "================Instance Summry Report All ================================="
    print "***Total instances count:\t%d" % (instance_monitor_summary_all.instances_count)
    print "***Total instances CPU count:\t%d" % (instance_monitor_summary_all.instances_cpu)
    print "***Total instances mem count:\t%d " % (instance_monitor_summary_all.instances_mem)
    print "***Running instances count:\t%d" % (instance_monitor_summary_all.running_instances_count)
    print "***Running instances CPU count:\t%d " % (instance_monitor_summary_all.running_instances_cpu)
    print "***Running instances mem count:\t%d GB" % (instance_monitor_summary_all.running_instances_mem)


#  Setting configuration
#  Default path for configuration file is "~/.oci/config"
config = oci.config.from_file()
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

#  For each region get the logs for each compartment.
compute_client.base_client.set_region('us-ashburn-1')
get_all_instances(compute_client, compartments)
#print get_all_shapes(compute_client,compartments)
#print get_all_volumes(block_storage_client, compartments)
