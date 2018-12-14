# coding: utf-8
# Copyright (c) 2016, 2018, Oracle and/or its affiliates. All rights reserved.
from crontab import CronTab
import oci
from oci.identity.models import AddUserToGroupDetails, CreateGroupDetails, CreateUserDetails, CreateCompartmentDetails
import ConfigParser
import sys
def get_monitored_compartments(identity, tenancy_id):
    '''
    Retrieve the list of compartments under the tenancy.
    '''
    monitored_compartment = {"apac_root_compartment":None, "emea_root_compartment": None, "amer_root_compartment": None}
    #  Store tenancy id as the first compartment
    # compartment_ocids.append(tenancy_id)
    #compartment_ocids.append(identity.get_compartment(tenancy_id).data)
    list_compartments_response = oci.pagination.list_call_get_all_results(
        identity.list_compartments,
        compartment_id=tenancy_id,
        compartment_id_in_subtree=False).data
    for c in list_compartments_response:
        ##compartment_ocids.append(c.id)
        if c.lifecycle_state == "ACTIVE":
            if c.name == 'SectionOne_DevOps_AMER':
                monitored_compartment["amer_root_compartment"] = c.id
            if c.name == 'SectionOne_DevOps_EMEA':
                monitored_compartment["emea_root_compartment"] = c.id
            if c.name == 'SectionOne_DevOps_APAC':
                monitored_compartment["apac_root_compartment"] = c.id
    
    if monitored_compartment["apac_root_compartment"] is None:
        monitored_compartment["apac_root_compartment"] = create_compartment(identity, tenancy_id, 'APAC')
    if monitored_compartment["emea_root_compartment"] is None:
        monitored_compartment["emea_root_compartment"] = create_compartment(identity, tenancy_id, 'EMEA')
    if monitored_compartment["amer_root_compartment"] is None:
        monitored_compartment["amer_root_compartment"] = create_compartment(identity, tenancy_id, 'AMER')
    
    return monitored_compartment

def create_compartment(identity, tenancy_id, key_name):
    cd_name = 'SectionOne_DevOps_' + key_name
    cd_description = " This compartment is used for monitor %s shift operations " % (key_name)
    compartment_details = CreateCompartmentDetails()
    compartment_details.compartment_id = tenancy_id
    compartment_details.name = cd_name
    compartment_details.description = cd_description
    new_c = identity.create_compartment(compartment_details).data
    return new_c.id

def write_config(section_name, value_list):
    cf = ConfigParser.ConfigParser()
    try:
        cf.read('/home/opc/.oci/config')
        #https://docs.python.org/2/library/configparser.html default pool will not be here
        if not cf.has_section(section_name):
            cf.add_section(section_name)
        for key, value in value_list.items():
            cf.set(section_name, key, value)
        cfgfile = open('/home/opc/.oci/config','w')
        cf.write(cfgfile)
        cfgfile.close()
    finally:
        pass

def create_cron(tenancy_name):
    cron = CronTab(user='opc')
    job_c1 = '/usr/bin/python /home/opc/OCI/oci-python-sdk/examples/retrieve_compute_details.py %s >> /tmp/%s_usage 2>&1' % (tenancy_name, tenancy_name)
    job_c2 = '/usr/bin/python /home/opc/OCI/oci-python-sdk/examples/retrieve_audit_events.py %s >> /tmp/%s_usage 2>&1' % (tenancy_name, tenancy_name)
    job_c3 = '/usr/bin/python /home/opc/OCI/oci-python-sdk/examples/shutdown_compute_in_specified_time.py %s >> /tmp/%s_usage 2>&1' % (tenancy_name, tenancy_name)
    job1 = cron.new(command = job_c1)
    job2 = cron.new(command = job_c2)
    job3 = cron.new(command = job_c3)
    job1.setall("31 */4 * * *")
    job2.setall("31 */4 * * *")
    job3.setall("31 */1 * * *")
    cron.write()

def usage():
    print 'usage: python new_tenancies_init.py <tenancy_ocid> <user_ocid>'

def delete_cron(tenany_name):
    pass
# Default config file and profile
#config = oci.config.from_file()
#config = oci.config.from_file(file_location='~/.oci/gse00015003', profile_name = "gse00015003")
config = {'region': 'us-ashburn-1', 'user': 'ocid1.user.oc1..aaaaaaaavmpzkgf5j6rwridbjox67wm7fctnjgg6g43bmmokiroqewqtnmya', 'log_requests': False, 'tenancy': 'ocid1.tenancy.oc1..aaaaaaaaqrol7kkrruav76ou65we6n4yj646gdt554ssiecdpqorr4jnyz7a', 'pass_phrase': None, 'fingerprint': '7a:4b:10:a2:5e:bf:d2:c0:d6:8c:0c:f7:27:6f:c7:7a', 'key_file': '/home/opc/.oci/oci_api_key.pem'} 
if len(sys.argv) == 3:
    config[tenancy] = sys.argv[1]
    config[user] = sys.argv[2]
elif len(sys.argv) == 1:
    print "this is used for testing purpose, will delete soon after production"
    usage()
    # this is only used for testing for nwo
else:
    print 'parameter error'
    usage()
    sys.exit(1)


tenancy_id = config["tenancy"] 
identity = oci.identity.IdentityClient(config)
root_compartment = identity.get_compartment(tenancy_id).data
tenancy_name = root_compartment.name
compartments = get_monitored_compartments(identity, tenancy_id)
merge_dict = dict(config, **compartments)
merge_dict['email_password'] = 'kkcmkeajiehcbzkf'
merge_dict['apac_shift_hours'] = [0,1,2,3,4,5,6,7,8,9,10,11,12]
merge_dict['emea_shift_hours'] = [8,9,10,11,12,13,14,15,16]
merge_dict['amer_shift_hours'] = [16,17,18,19,20,21,22,23,0]
merge_dict['to_list'] = 'mike.cao@oracle.com,vipmike007@gmail.com'
merge_dict['cc_list'] = ''
merge_dict['special_compartment'] = 'ocid1.compartment.oc1..aaaaaaaa3hg6hurigmr4bdbngby6dcjiug24f2s4p5zpqw3akafe7in5cxua'

# Service client
#step1 getall compartment under root, if it has 

# write config file to the disk
#https://www.cnblogs.com/feeland/p/4514771.html
write_config(tenancy_name, merge_dict)
# create crontab automately
#https://stackoverflow.com/questions/30318168/python-how-to-handle-crontab-comman
create_cron(tenancy_name)
