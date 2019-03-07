# coding: utf-8
# Copyright (c) 2016, 2019, Oracle and/or its affiliates. All rights reserved.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class CertificateSummary(object):
    """
    A summary of the SSL certificate's information.
    **Warning:** Oracle recommends that you avoid using any confidential information when you supply string values using the API.
    """

    #: A constant which can be used with the lifecycle_state property of a CertificateSummary.
    #: This constant has a value of "CREATING"
    LIFECYCLE_STATE_CREATING = "CREATING"

    #: A constant which can be used with the lifecycle_state property of a CertificateSummary.
    #: This constant has a value of "ACTIVE"
    LIFECYCLE_STATE_ACTIVE = "ACTIVE"

    #: A constant which can be used with the lifecycle_state property of a CertificateSummary.
    #: This constant has a value of "FAILED"
    LIFECYCLE_STATE_FAILED = "FAILED"

    #: A constant which can be used with the lifecycle_state property of a CertificateSummary.
    #: This constant has a value of "UPDATING"
    LIFECYCLE_STATE_UPDATING = "UPDATING"

    #: A constant which can be used with the lifecycle_state property of a CertificateSummary.
    #: This constant has a value of "DELETING"
    LIFECYCLE_STATE_DELETING = "DELETING"

    #: A constant which can be used with the lifecycle_state property of a CertificateSummary.
    #: This constant has a value of "DELETED"
    LIFECYCLE_STATE_DELETED = "DELETED"

    def __init__(self, **kwargs):
        """
        Initializes a new CertificateSummary object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param id:
            The value to assign to the id property of this CertificateSummary.
        :type id: str

        :param compartment_id:
            The value to assign to the compartment_id property of this CertificateSummary.
        :type compartment_id: str

        :param display_name:
            The value to assign to the display_name property of this CertificateSummary.
        :type display_name: str

        :param time_not_valid_after:
            The value to assign to the time_not_valid_after property of this CertificateSummary.
        :type time_not_valid_after: datetime

        :param freeform_tags:
            The value to assign to the freeform_tags property of this CertificateSummary.
        :type freeform_tags: dict(str, str)

        :param defined_tags:
            The value to assign to the defined_tags property of this CertificateSummary.
        :type defined_tags: dict(str, dict(str, object))

        :param lifecycle_state:
            The value to assign to the lifecycle_state property of this CertificateSummary.
            Allowed values for this property are: "CREATING", "ACTIVE", "FAILED", "UPDATING", "DELETING", "DELETED", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type lifecycle_state: str

        :param time_created:
            The value to assign to the time_created property of this CertificateSummary.
        :type time_created: datetime

        """
        self.swagger_types = {
            'id': 'str',
            'compartment_id': 'str',
            'display_name': 'str',
            'time_not_valid_after': 'datetime',
            'freeform_tags': 'dict(str, str)',
            'defined_tags': 'dict(str, dict(str, object))',
            'lifecycle_state': 'str',
            'time_created': 'datetime'
        }

        self.attribute_map = {
            'id': 'id',
            'compartment_id': 'compartmentId',
            'display_name': 'displayName',
            'time_not_valid_after': 'timeNotValidAfter',
            'freeform_tags': 'freeformTags',
            'defined_tags': 'definedTags',
            'lifecycle_state': 'lifecycleState',
            'time_created': 'timeCreated'
        }

        self._id = None
        self._compartment_id = None
        self._display_name = None
        self._time_not_valid_after = None
        self._freeform_tags = None
        self._defined_tags = None
        self._lifecycle_state = None
        self._time_created = None

    @property
    def id(self):
        """
        Gets the id of this CertificateSummary.
        The `OCID`__ of the SSL certificate.

        __ https://docs.us-phoenix-1.oraclecloud.com/Content/General/Concepts/identifiers.htm


        :return: The id of this CertificateSummary.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this CertificateSummary.
        The `OCID`__ of the SSL certificate.

        __ https://docs.us-phoenix-1.oraclecloud.com/Content/General/Concepts/identifiers.htm


        :param id: The id of this CertificateSummary.
        :type: str
        """
        self._id = id

    @property
    def compartment_id(self):
        """
        Gets the compartment_id of this CertificateSummary.
        The `OCID`__ of the SSL certificate's compartment.

        __ https://docs.us-phoenix-1.oraclecloud.com/Content/General/Concepts/identifiers.htm


        :return: The compartment_id of this CertificateSummary.
        :rtype: str
        """
        return self._compartment_id

    @compartment_id.setter
    def compartment_id(self, compartment_id):
        """
        Sets the compartment_id of this CertificateSummary.
        The `OCID`__ of the SSL certificate's compartment.

        __ https://docs.us-phoenix-1.oraclecloud.com/Content/General/Concepts/identifiers.htm


        :param compartment_id: The compartment_id of this CertificateSummary.
        :type: str
        """
        self._compartment_id = compartment_id

    @property
    def display_name(self):
        """
        Gets the display_name of this CertificateSummary.
        The user-friendly name of the SSL certificate.


        :return: The display_name of this CertificateSummary.
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """
        Sets the display_name of this CertificateSummary.
        The user-friendly name of the SSL certificate.


        :param display_name: The display_name of this CertificateSummary.
        :type: str
        """
        self._display_name = display_name

    @property
    def time_not_valid_after(self):
        """
        Gets the time_not_valid_after of this CertificateSummary.
        The date and time the certificate will expire, expressed in RFC 3339 timestamp format.


        :return: The time_not_valid_after of this CertificateSummary.
        :rtype: datetime
        """
        return self._time_not_valid_after

    @time_not_valid_after.setter
    def time_not_valid_after(self, time_not_valid_after):
        """
        Sets the time_not_valid_after of this CertificateSummary.
        The date and time the certificate will expire, expressed in RFC 3339 timestamp format.


        :param time_not_valid_after: The time_not_valid_after of this CertificateSummary.
        :type: datetime
        """
        self._time_not_valid_after = time_not_valid_after

    @property
    def freeform_tags(self):
        """
        Gets the freeform_tags of this CertificateSummary.
        A simple key-value pair without any defined schema.


        :return: The freeform_tags of this CertificateSummary.
        :rtype: dict(str, str)
        """
        return self._freeform_tags

    @freeform_tags.setter
    def freeform_tags(self, freeform_tags):
        """
        Sets the freeform_tags of this CertificateSummary.
        A simple key-value pair without any defined schema.


        :param freeform_tags: The freeform_tags of this CertificateSummary.
        :type: dict(str, str)
        """
        self._freeform_tags = freeform_tags

    @property
    def defined_tags(self):
        """
        Gets the defined_tags of this CertificateSummary.
        A key-value pair with a defined schema that restricts the values of tags. These predefined keys are scoped to namespaces.


        :return: The defined_tags of this CertificateSummary.
        :rtype: dict(str, dict(str, object))
        """
        return self._defined_tags

    @defined_tags.setter
    def defined_tags(self, defined_tags):
        """
        Sets the defined_tags of this CertificateSummary.
        A key-value pair with a defined schema that restricts the values of tags. These predefined keys are scoped to namespaces.


        :param defined_tags: The defined_tags of this CertificateSummary.
        :type: dict(str, dict(str, object))
        """
        self._defined_tags = defined_tags

    @property
    def lifecycle_state(self):
        """
        Gets the lifecycle_state of this CertificateSummary.
        The current lifecycle state of the certificate.

        Allowed values for this property are: "CREATING", "ACTIVE", "FAILED", "UPDATING", "DELETING", "DELETED", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The lifecycle_state of this CertificateSummary.
        :rtype: str
        """
        return self._lifecycle_state

    @lifecycle_state.setter
    def lifecycle_state(self, lifecycle_state):
        """
        Sets the lifecycle_state of this CertificateSummary.
        The current lifecycle state of the certificate.


        :param lifecycle_state: The lifecycle_state of this CertificateSummary.
        :type: str
        """
        allowed_values = ["CREATING", "ACTIVE", "FAILED", "UPDATING", "DELETING", "DELETED"]
        if not value_allowed_none_or_none_sentinel(lifecycle_state, allowed_values):
            lifecycle_state = 'UNKNOWN_ENUM_VALUE'
        self._lifecycle_state = lifecycle_state

    @property
    def time_created(self):
        """
        Gets the time_created of this CertificateSummary.
        The date and time the certificate was created, in the format defined by RFC3339.


        :return: The time_created of this CertificateSummary.
        :rtype: datetime
        """
        return self._time_created

    @time_created.setter
    def time_created(self, time_created):
        """
        Sets the time_created of this CertificateSummary.
        The date and time the certificate was created, in the format defined by RFC3339.


        :param time_created: The time_created of this CertificateSummary.
        :type: datetime
        """
        self._time_created = time_created

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
