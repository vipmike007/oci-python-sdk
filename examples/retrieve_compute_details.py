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
    compartment_ocids.append(identity.get_compartment(tenancy_id).data)
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
    content = ["","","",0]
    content[0] = "================= Volume Block Device Usage Report========================\n"
    content[2] = "================Volume Summry Report Per Comparment=======================\n"
    for i in range(len(volume_summary_report)):
        volume_monitor_summary_all.instances_count += volume_summary_report[i].instances_count
        volume_monitor_summary_all.instances_mem += volume_summary_report[i].instances_mem
        content[2] += "*Compartment_name \t\t%s\n" % (volume_summary_report[i].oc.name)
        content[2] += "*Compartment DESC \t\t%s\n" % (volume_summary_report[i].oc.description)
        content[2] += "*Total volume count\t\t%d\n" % (volume_summary_report[i].instances_count)
        content[2] += "*Total Volume Size:\t\t%dGB\n\n" % (volume_summary_report[i].instances_mem)
  
    content[1] += "================Volume Summry Report in total=======================\n"
    content[1] += "*Total volume count\t\t%d\n" % (volume_monitor_summary_all.instances_count)
    content[1] += "*Total Volume Size\t\t%dGB\n" % (volume_monitor_summary_all.instances_mem)
    total_size = volume_monitor_summary_all.instances_mem*1024
    if total_size == 0:
        content[3] = 1
    elif total_size >0 and total_size <= 700:
        content[3] = 2
    elif total_size > 700 and total_size <= 900:
        content[3] = 3
    elif total_size > 900 and total_size <=1024:
        content[3] = 4
    elif total_size > 1024:
        content[3] = 5
    else:
        content[3] = 0

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

def send_report_out(subject, content, to_list, cc_list):
    email_client = email_notification.Email()
    email_client.mailto_list = to_list
    email_client.mailcc_list = cc_list
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
    content = ["", "", "", 0]
    content[0] = "================Instance Summry Report ========================\n"
    content[2] = "================VM instances usage per compartment ===============\n"
    for i in range(len(instance_summary_report)):
        instance_monitor_summary_all.instances_count += instance_summary_report[i].instances_count
        instance_monitor_summary_all.instances_cpu += instance_summary_report[i].instances_cpu
        instance_monitor_summary_all.instances_mem += instance_summary_report[i].instances_mem
        instance_monitor_summary_all.running_instances_count += instance_summary_report[i].running_instances_count
        instance_monitor_summary_all.running_instances_cpu += instance_summary_report[i].running_instances_cpu
        instance_monitor_summary_all.running_instances_mem += instance_summary_report[i].running_instances_mem
        
        ##print results
        if instance_summary_report[i].running_instances_count !=0:
            content[2] += "*Compartment_name \t\t%s\n" % (instance_summary_report[i].oc.name)
            content[2] += "*Compartment DESC \t\t%s\n" % (instance_summary_report[i].oc.description)
            content[2]+= "*Total instances count:\t\t%d\n" % (instance_summary_report[i].instances_count)
            content[2] += "*Running instances count:\t%d\n" % (instance_summary_report[i].running_instances_count)
            content[2] += "*Total instances CPU count:\t%d\n" % (instance_summary_report[i].instances_cpu)
            content[2] += "*Total instances mem count:\t%d\n" % (instance_summary_report[i].instances_mem)
            content[2] += "*Running instances CPU count:\t%d\n" % (instance_summary_report[i].running_instances_cpu)
            content[2] += "*Running instances mem count:\t%d GB \n\n" % (instance_summary_report[i].running_instances_mem)
        else:
            content[2] += "*Compartment %s:\t 0|%d instances running\n\n" % (instance_summary_report[i].oc.name, instance_summary_report[i].instances_count)
        content[2] += "**************************************************************************\n"

    
    content[1] += "================Instance Summry Report All =================================\n"
    content[1] += "*Total instances count:\t%d\n" % (instance_monitor_summary_all.instances_count)
    content[1] += "*Total instances CPU count:\t%d\n" % (instance_monitor_summary_all.instances_cpu)
    content[1] += "*Total instances mem count:\t%d\n" % (instance_monitor_summary_all.instances_mem)
    content[1] += "*Running instances count:\t%d\n"% (instance_monitor_summary_all.running_instances_count)
    content[1] += "*Running instances CPU count:\t%d\n" % (instance_monitor_summary_all.running_instances_cpu)
    content[1] += "*Running instances mem count:\t%d GB\n" % (instance_monitor_summary_all.running_instances_mem)
    # judge if everything works fine
    if instance_monitor_summary_all.instances_count  == 0:
        content[3] = 1
    elif instance_monitor_summary_all.instances_count > 0 and instance_monitor_summary_all.instances_count <=8:
        content[3] = 2
    elif instance_monitor_summary_all.instances_count > 8 and instance_monitor_summary_all.instances_count <=10:
        content[3] = 3
    elif instance_monitor_summary_all.instances_count > 10 and instance_monitor_summary_all.instances_count <=12:
        content[3] = 4
    elif instance_monitor_summary_all.instances_count > 12:
        content[3] = 5
    else:
        content[3] = 0
    return content

def get_all_db_system(dbs, compartment_ocids):
    list_of_db_systems = []
    for c_object in compartment_ocids:
        c = c_object.id
        db_lists = oci.pagination.list_call_get_all_results(
            dbs.list_db_systems,
            compartment_id=c).data
        list_of_db_systems.extend(db_lists)
    content = ["", "", "", 0]
    count = 0
    size = 0
    cpu = 0
    special_monitoring = ""
    content[0] = "================ Database Summry Report ===========================\n"
    for i in list_of_db_systems:
        if i.lifecycle_state == "AVAILABLE" or i.lifecycle_state == "PROVISIONING":
            count += 1
            size += i.data_storage_size_in_gbs
            cpu += get_cpu_by_shape(i.shape)
            if i.database_edition != "STANDARD_EDITION":
                special_monitoring += "DB %s are using %s DB\n" %(i.display_name,i.database_edition)
    content[1] += "*Total DB count is %d \n" %(count)
    content[1] += "*Total DB cpu is %d \n" %(cpu)
    content[1] += "*Total DB extra storage size is %d \n" % (size)
    content[1] += special_monitoring

    if count == 0:
        content[3] = 1
    elif count > 0 and count <=2:
        content[3] = 2
    elif count > 2 and count <=3:
        content [3] = 3
    elif count > 3 and count <=4:
        content [3] = 4
    elif count >4 :
        content[3] = 5
    else:
        content[3] = 0
    
#    content = instance_handling(list_of_db_systems)
    return content
def get_all_buckets(object_storage_client, comparmments):
    namespace = object_storage_client.get_namespace().data
    object_buckets_list = []
    for i in compartments:
        object_buckets_list.extend(object_storage_client.list_buckets(namespace, i.id).data)
    return object_buckets_list

def get_all_object_size(object_storage_client, buckets):
    content = ["","","", 0]
    content[0] =  "  ================OBJECT Summry Report ========================\n"
    content[1] = "*total object size: \t "
    namespace = object_storage_client.get_namespace().data
    object_list = []
    total_size = 0.000000000000000000000000
    for i in buckets:
        o_list=object_storage_client.list_objects(namespace, i.name,fields='name,size,timeCreated,md5').data.objects
        object_list.extend(o_list)
    for i in object_list:
        total_size += i.size/1048576.000000000
    content[1] = content[1] + str(total_size) + " MB\n"

    total_size = total_size/1024.000000000
    
    if total_size == 0:
        content[3] = 1
    elif total_size >0 and total_size <= 700:
        content[3] = 2
    elif total_size > 700 and total_size <= 900:
        content[3] = 3
    elif total_size > 900 and total_size <=1024:
        content[3] = 4
    elif total_size > 1024:
        content[3] = 5
    else:
        content[3] = 0

    return content

def check_storage_summary(nfs_storage_client, compartments, identity):
    #get list of availability domain first
    size = 0
    content = ["", "", "", 0]
    content[0] =  "  ================FSS(nfs) Summry Report ========================\n"
    content[1] += "*total File System service size: \t "

    for c in compartments:
        a_domain_s = identity.list_availability_domains(c.id).data
        for a in a_domain_s:
            summary_list = nfs_storage_client.list_file_systems(c.id, a.name).data
            if len(summary_list) != 0:
                for j in summary_list:
                    size += j.metered_bytes

    total_size = size / 1048576.000000000/ 1024.00000
    content[1] = content[1] + str(total_size) + " GB\n"
    if total_size ==0:
        content[3] = 1
    elif total_size >0 and total_size <= 700:
        content[3] = 2
    elif total_size > 700 and total_size <= 900:
        content[3] = 3
    elif total_size > 900 and total_size <=1024:
        content[3] = 4
    elif total_size > 1024:
        content[3] = 5
    else:
        content[3] = 0


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
elif len(sys.argv) == 3:
    config = oci.config.from_file(file_location='~/.oci/config', profile_name = sys.argv[1])
    tenancy_name = sys.argv[1]
    email_sent = False
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

DS_status={1 :'No Use - All Good' , 
           2: 'in Use - All Good', 
           3: 'Warning - Need review' , 
           4: 'Fatal alerts - Need review', 
           5: 'OverLoaded - Need Action ASAP',
           0: 'Scripts Error - Contact Mike.Cao to check the RCA'}
compute_client = oci.core.ComputeClient(config)
shape = oci.core.models.Shape()
block_storage_client = oci.core.BlockstorageClient(config)
db_client = oci.database.DatabaseClient(config)
object_storage_client = oci.object_storage.ObjectStorageClient(config)
nfs_storage_client = oci.file_storage.FileStorageClient(config)
db_client.base_client.set_region('us-ashburn-1')

to_list=(str(config["to_list"])).split(',')
cc_list=(str(config["cc_list"])).split(',')


#  For each region get the logs for each compartment.
compute_client.base_client.set_region('us-ashburn-1')
content = ""
report_status_id = 0
instance_content = get_all_instances(compute_client, compartments)
if instance_content[3] > report_status_id:
    report_status_id = instance_content[3]

content = content + instance_content[0] + instance_content[1]
if instance_content[3] != 1 and instance_content[3] != 2:
    content = content + instance_content[2]

db_content = get_all_db_system(db_client,compartments)
if db_content[3] > report_status_id:
    report_status_id = db_content[3]
## DB do not support check per compartments
content = content + db_content[0] + db_content[1]


volume_content = get_all_volumes(block_storage_client, compartments)
if volume_content[3] > report_status_id:
    report_status_id = volume_content[3]
content = content + volume_content[0] + volume_content[1]
if volume_content[3] != 1 and volume_content[3] != 2:
    content = content + volume_content[2]

### support object 
buckets = get_all_buckets(object_storage_client, compartments)
object_content = get_all_object_size(object_storage_client,  buckets)
if object_content[3] > report_status_id:
    report_status_id = object_content[3]
content = content + object_content[0] + object_content[1]

nfs_storage = check_storage_summary(nfs_storage_client, compartments, identity)
if nfs_storage[3] > report_status_id:
    report_status_id = nfs_storage[3]
content = content + nfs_storage[0] + nfs_storage[1]

print DS_status[report_status_id]
print content
send_report_out("Tenancy - " + tenancy_name + "-"+datetime.datetime.utcnow().strftime("%Y-%m-%d-%H:%M") + ' - ' + DS_status[report_status_id],content,to_list,cc_list)

