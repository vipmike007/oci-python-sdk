# coding: utf-8
# Copyright (c) 2016, 2018, Oracle and/or its affiliates. All rights reserved.

#  This script retrieves all audit logs across an Oracle Cloud Infrastructure Tenancy.
#  for a timespan defined by start_time and end_time.
#  Last Modifed by: Mike Cao <mike.cao@oracle.com>
#  Time : 05-Nov-2018

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
    #compartment_ocids.append(tenancy_id)
    list_compartments_response = oci.pagination.list_call_get_all_results(
        identity.list_compartments,
        compartment_id=tenancy_id,
        compartment_id_in_subtree=True).data
    for c in list_compartments_response:
        #compartment_ocids.append(c.id)
        if c.lifecycle_state == "ACTIVE":
            compartment_ocids.append(c)
    return compartment_ocids

class audit_per_c:
    def __init__(self):
        self.compartment_name = ""
        self.response_time = ""
        self.user_name = ""
        self.event_name = ""
        self.event_time = ""
        self.event_request_action = ""

def send_report_out(subject, content):
    email_client = email_notification.Email()
    email_client.send_mail(subject, content)

def audit_handling(data):
    list_audits=[]
    audit_instance = audit_per_c()
    content = "event_time\t\tevent_name\t\ttype\tusername\n"
    for i in range(len(data)):
        if data[i].request_action != "GET":
            audit_instance.compartment_name = data[i].compartment_name
            audit_instance.response_time = data[i].response_time
            audit_instance.user_name = data[i].user_name
            audit_instance.event_name = data[i].event_name
            audit_instance.event_time = data[i].event_time
            audit_instance.request_action = data[i].request_action
            #print data[i].request_action
            content += "%s\t%s\t\t%s\t%s \n" % (data[i].event_time.strftime("%Y-%m-%d-%H:%M:%S"), data[i].event_name,  data[i].request_action, data[i].user_name)
            list_audits.append(audit_instance)
    return content
    #email = email_notification.Email()
    #email.send_mail("Audit Report Events_Time"+datetime.datetime.utcnow().strftime("%Y-%m-%d-%H:%M:%S"),content)
    # print content
    #return(list_audits)


def get_audit_events(audit, compartment_ocids, start_time, end_time):
    '''
    Get events iteratively for each compartment defined in 'compartments_ocids'
    for the region defined in 'audit'.
    This method eagerly loads all audit records in the time range and it does
    have performance implications of lot of audit records.
    Ideally, the generator method in oci.pagination should be used to lazily
    load results.
    '''
    list_of_audit_events = []
    for c_object in compartment_ocids:
        c = c_object.id
        list_events_response = oci.pagination.list_call_get_all_results(
            audit.list_events,
            compartment_id=c,
            start_time=start_time,
            end_time=end_time).data
       # print list_events_response
        #list_events_response = audit.list_events(
         #       compartment_id = c,
          #      start_time = start_time,
           #     end_time = end_time)
        #  Results for a compartment 'c' for a region defined
        #  in 'audit' object.
        # list_of_audit_events.extend(list_events_response)
        list_of_audit_events.extend(list_events_response)
    content = audit_handling(list_of_audit_events)
    return content
    #return str(list_of_audit_events)

        
   #print type(list_of_audit_events[3])     #print list_of_audit_events[3]
        #return list_of_audit_events


#  Setting configuration
#  Default path for configuration file is "~/.oci/config"
#config = oci.config.from_file()
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

#  Timespan defined by variables start_time and end_time(today).
#  ListEvents expects timestamps into RFC3339 format.
#  For the purposes of sample script, logs of last 1 days.
end_time = datetime.datetime.utcnow()
#start_time = end_time + datetime.timedelta(days=-1)
start_time = end_time + datetime.timedelta(hours=-12)

# This array will be used to store the list of available regions.
regions = get_regions(identity)

# This array will be used to store the list of compartments in the tenancy.
compartments = get_compartments(identity, tenancy_id)

for i in range(len(compartments)):
    print compartments[i].name
audit = oci.audit.audit_client.AuditClient(config)

#  For each region get the logs for each compartment.
#for r in regions:
    #  Intialize with a region value.
    #audit.base_client.set_region(r)
audit.base_client.set_region('us-ashburn-1')
#  To separate results by region use print here.
audit_events = get_audit_events(
        audit,
        compartments,
        start_time,
        end_time)

send_report_out("Operation Audit Report - "+datetime.datetime.utcnow().strftime("%Y-%m-%d-%H:%M"),audit_events)



    #  Results for a region 'r' for each compartment.
   # if audit_events:
    #    print(audit_events)
