# coding: utf-8
# Copyright (c) 2016, 2018, Oracle and/or its affiliates. All rights reserved.

import oci
from oci.identity.models import AddUserToGroupDetails, CreateGroupDetails, CreateUserDetails, CreateCompartmentDetails
import ConfigParser
def get_compartments(identity, tenancy_id):
    '''
    Retrieve the list of compartments under the tenancy.
    '''
    monitored_compartment = {"apac":None, "emea": None, "amer": None}
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
                monitored_compartment["amer"] = c.id
            if c.name == 'SectionOne_DevOps_EMEA':
                monitored_compartment["emea"] = c.id
            if c.name == 'SectionOne_DevOps_APAC':
                monitored_compartment["apac"] = c.id
    
    if monitored_compartment["apac"] is None:
        monitored_compartment["apac"] = create_compartment(identity, tenancy_id, 'APAC')
    if monitored_compartment["emea"] is None:
        monitored_compartment["emea"] = create_compartment(identity, tenancy_id, 'EMEA')
    if monitored_compartment["amer"] is None:
        monitored_compartment["amer"] = create_compartment(identity, tenancy_id, 'AMER')
    
    return monitored_compartment

def create_compartment(identity, tenancy_id, key_name):
    cd_name = 'SectionOne_DevOps_' + key_name
    print cd_name
    cd_description = " This compartment is used for monitor %s shift operations " % (key_name)
    compartment_details = CreateCompartmentDetails()
    compartment_details.compartment_id = tenancy_id
    compartment_details.name = cd_name
    compartment_details.description = cd_description
    new_c = identity.create_compartment(compartment_details).data
    return new_c.id

def write_config():
    cf = ConfigParser.ConfigParser()
    cf.read('/home/opc/.oci/config')
    #https://docs.python.org/2/library/configparser.html default pool will not be here
    secs = cf.sections()
    print cf.options(secs[0])
    # in the future will use if to judge this part
    #opts = cf.options("DEFAULT")
   # cf.write('~/.oci/config_init2')
    cfgfile = open('/home/opc/.oci/config_init2','w')
    cf.add_section("section1")
    cf.set("section1", 'user','ocid1.user.oc1..aaaaaaaavmpzkgf5j6rwridbjox67wm7fctnjgg6g43bmmokiroqewqtnmya')
    cf.set("section1", 'cc_list', '')
    cf.write(cfgfile)
    cfgfile.close()

# Default config file and profile
#config = oci.config.from_file()
#config = oci.config.from_file(file_location='~/.oci/gse00015003', profile_name = "gse00015003")
config = {'region': 'us-ashburn-1', 'user': 'ocid1.user.oc1..aaaaaaaavmpzkgf5j6rwridbjox67wm7fctnjgg6g43bmmokiroqewqtnmya', 'log_requests': False, 'tenancy': 'ocid1.tenancy.oc1..aaaaaaaaqrol7kkrruav76ou65we6n4yj646gdt554ssiecdpqorr4jnyz7a', 'pass_phrase': None, 'fingerprint': '7a:4b:10:a2:5e:bf:d2:c0:d6:8c:0c:f7:27:6f:c7:7a', 'key_file': '/home/opc/.oci/oci_api_key.pem'}

tenancy_id = config["tenancy"] 
print type(config)
identity = oci.identity.IdentityClient(config)
#print identity
#identity.set_region('us-ashburn-1')

compartments = get_compartments(identity, tenancy_id)
print compartments
# Service client
#step1 getall compartment under root, if it has 

# write config file to the disk
#https://www.cnblogs.com/feeland/p/4514771.html
#write_config()
# create crontab automately
#https://stackoverflow.com/questions/30318168/python-how-to-handle-crontab-comman
