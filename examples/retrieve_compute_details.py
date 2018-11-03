# coding: utf-8
# Copyright (c) 2016, 2018, Oracle and/or its affiliates. All rights reserved.

#  This script retrieves all audit logs across an Oracle Cloud Infrastructure Tenancy.
#  for a timespan defined by start_time and end_time.
#  This sample script retrieves Audit events for last 5 days.
#  This script will work at a tenancy level only.

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
    compartment_ocids.append(tenancy_id)
    list_compartments_response = oci.pagination.list_call_get_all_results(
        identity.list_compartments,
        compartment_id=tenancy_id).data
    for c in list_compartments_response:
        compartment_ocids.append(c.id)
    return compartment_ocids

def get_shape_detals(shape_name):
    pass

def get_all_shapes(compute_client, compartment_ocids):

    for c in compartment_ocids:
        list_shapes = compute_client.list_shapes(c)
        data = list_shapes.data
        while list_shapes.has_next_page:
            list_shapes = compute_client(c, page=list_shapes.next_page)
            data.extend(list_shapes.data)
            print 'shap is here hahahahaha'
        print data
        return data

def get_all_instances(compute, compartment_ocids):
    '''
    Get events iteratively for each compartment defined in 'compartments_ocids'
    for the region defined in 'compute'.
    '''
    for c in compartment_ocids:
        #c='ocid1.compartment.oc1..aaaaaaaa3hg6hurigmr4bdbngby6dcjiug24f2s4p5zpqw3akafe7in5cxua'
        list_computes = compute.list_instances(c)
        data = list_computes.data
        while list_computes.has_next_page:
            list_computes = compute.list_instances(c, page=list_computes.next_page)
            data.extend(list_computes.data)
            print 'hahahahahahahahahh'
        print c
        print type(c)
        print type(data)
        print data

        #  Results for a compartment 'c' for a region defined
        #  in 'audit' object.
    return data


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

#  For each region get the logs for each compartment.
compute_client.base_client.set_region('us-ashburn-1')
print get_all_instances(compute_client, compartments)
print get_all_shapes(compute_client,compartments)
print help(shape)
print shape.shape('VM.Standard1.2')

