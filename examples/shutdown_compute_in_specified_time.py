#!/usr/bin/python
# coding: utf-8
# Written by: Mike Cao <mike.cao@oracle.com>
# Version 1.0 - 04-Nov-2018
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
    #  Store tenancy id as the first compartment
    print name
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




def instance_shutdown(data, instance_handle):
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

def send_report_out(subject, content):
    email_client = email_notification.Email()
    email_client.send_mail(subject, content)

def stop_all_instances(compute, compartment_ocids):
    '''
    Get events iteratively for each compartment defined in 'compartments_ocids'
    for the region defined in 'compute'.
    '''
    instance_summary_report = []

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
                print type(instance)
                oci.wait_until(compute,compute_client.get_instance(instance.id),'lifecycle_state','STOPPED',succeed_on_not_found=True)
                print instance.display_name + "is stopped"

#  Setting configuration
#  Default path for configuration file is "~/.oci/config"
config = oci.config.from_file()
tenancy_id = config["tenancy"]

#  Initiate the client with the locally available config.
identity = oci.identity.IdentityClient(config)

# This array will be used to store the list of available regions.
regions = get_regions(identity)

compartments_list = []
#this compartment is hardcode
SectionOneRootCompartment='ocid1.compartment.oc1..aaaaaaaa66fpv7qdgx6hcqrxlrnzyeqzxermw5ywqx6jlxiepme6vtkjlzxq'
compartments = get_compartments(identity, SectionOneRootCompartment, compartments_list,"root")


compute_client = oci.core.ComputeClient(config)
shape = oci.core.models.Shape()
block_storage_client = oci.core.BlockstorageClient(config)

#  For each region get the logs for each compartment.
compute_client.base_client.set_region('us-ashburn-1')
stop_all_instances(compute_client, compartments)
#content = get_all_instances(compute_client, compartments)
#send_report_out("Compute Audit Report -"+datetime.datetime.utcnow().strftime("%Y-%m-%d-%H:%M"),content)
#print get_all_shapes(compute_client,compartments)
#content = get_all_volumes(block_storage_client, compartments)
#send_report_out("Block Audit Report -"+datetime.datetime.utcnow().strftime("%Y-%m-%d-%H:%M"),content)


