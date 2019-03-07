# coding: utf-8
# Copyright (c) 2016, 2019, Oracle and/or its affiliates. All rights reserved.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class CreateStreamDetails(object):
    """
    Object used to create a stream.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new CreateStreamDetails object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param name:
            The value to assign to the name property of this CreateStreamDetails.
        :type name: str

        :param partitions:
            The value to assign to the partitions property of this CreateStreamDetails.
        :type partitions: int

        :param compartment_id:
            The value to assign to the compartment_id property of this CreateStreamDetails.
        :type compartment_id: str

        :param retention_in_hours:
            The value to assign to the retention_in_hours property of this CreateStreamDetails.
        :type retention_in_hours: int

        :param freeform_tags:
            The value to assign to the freeform_tags property of this CreateStreamDetails.
        :type freeform_tags: dict(str, str)

        :param defined_tags:
            The value to assign to the defined_tags property of this CreateStreamDetails.
        :type defined_tags: dict(str, dict(str, object))

        """
        self.swagger_types = {
            'name': 'str',
            'partitions': 'int',
            'compartment_id': 'str',
            'retention_in_hours': 'int',
            'freeform_tags': 'dict(str, str)',
            'defined_tags': 'dict(str, dict(str, object))'
        }

        self.attribute_map = {
            'name': 'name',
            'partitions': 'partitions',
            'compartment_id': 'compartmentId',
            'retention_in_hours': 'retentionInHours',
            'freeform_tags': 'freeformTags',
            'defined_tags': 'definedTags'
        }

        self._name = None
        self._partitions = None
        self._compartment_id = None
        self._retention_in_hours = None
        self._freeform_tags = None
        self._defined_tags = None

    @property
    def name(self):
        """
        **[Required]** Gets the name of this CreateStreamDetails.
        The name of the stream. Avoid entering confidential information.

        Example: `TelemetryEvents`


        :return: The name of this CreateStreamDetails.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this CreateStreamDetails.
        The name of the stream. Avoid entering confidential information.

        Example: `TelemetryEvents`


        :param name: The name of this CreateStreamDetails.
        :type: str
        """
        self._name = name

    @property
    def partitions(self):
        """
        **[Required]** Gets the partitions of this CreateStreamDetails.
        The number of partitions in the stream.


        :return: The partitions of this CreateStreamDetails.
        :rtype: int
        """
        return self._partitions

    @partitions.setter
    def partitions(self, partitions):
        """
        Sets the partitions of this CreateStreamDetails.
        The number of partitions in the stream.


        :param partitions: The partitions of this CreateStreamDetails.
        :type: int
        """
        self._partitions = partitions

    @property
    def compartment_id(self):
        """
        **[Required]** Gets the compartment_id of this CreateStreamDetails.
        The OCID of the compartment that contains the stream.


        :return: The compartment_id of this CreateStreamDetails.
        :rtype: str
        """
        return self._compartment_id

    @compartment_id.setter
    def compartment_id(self, compartment_id):
        """
        Sets the compartment_id of this CreateStreamDetails.
        The OCID of the compartment that contains the stream.


        :param compartment_id: The compartment_id of this CreateStreamDetails.
        :type: str
        """
        self._compartment_id = compartment_id

    @property
    def retention_in_hours(self):
        """
        Gets the retention_in_hours of this CreateStreamDetails.
        The retention period of the stream, in hours. Accepted values are between 24 and 168 (7 days).
        If not specified, the stream will have a retention period of 24 hours.


        :return: The retention_in_hours of this CreateStreamDetails.
        :rtype: int
        """
        return self._retention_in_hours

    @retention_in_hours.setter
    def retention_in_hours(self, retention_in_hours):
        """
        Sets the retention_in_hours of this CreateStreamDetails.
        The retention period of the stream, in hours. Accepted values are between 24 and 168 (7 days).
        If not specified, the stream will have a retention period of 24 hours.


        :param retention_in_hours: The retention_in_hours of this CreateStreamDetails.
        :type: int
        """
        self._retention_in_hours = retention_in_hours

    @property
    def freeform_tags(self):
        """
        Gets the freeform_tags of this CreateStreamDetails.
        Free-form tags for this resource. Each tag is a simple key-value pair that is applied with no predefined name, type, or namespace. Exists for cross-compatibility only.
        For more information, see `Resource Tags`__.

        Example: `{\"Department\": \"Finance\"}`

        __ https://docs.us-phoenix-1.oraclecloud.com/Content/General/Concepts/resourcetags.htm


        :return: The freeform_tags of this CreateStreamDetails.
        :rtype: dict(str, str)
        """
        return self._freeform_tags

    @freeform_tags.setter
    def freeform_tags(self, freeform_tags):
        """
        Sets the freeform_tags of this CreateStreamDetails.
        Free-form tags for this resource. Each tag is a simple key-value pair that is applied with no predefined name, type, or namespace. Exists for cross-compatibility only.
        For more information, see `Resource Tags`__.

        Example: `{\"Department\": \"Finance\"}`

        __ https://docs.us-phoenix-1.oraclecloud.com/Content/General/Concepts/resourcetags.htm


        :param freeform_tags: The freeform_tags of this CreateStreamDetails.
        :type: dict(str, str)
        """
        self._freeform_tags = freeform_tags

    @property
    def defined_tags(self):
        """
        Gets the defined_tags of this CreateStreamDetails.
        Defined tags for this resource. Each key is predefined and scoped to a namespace. For more information, see `Resource Tags`__.

        Example: `{\"Operations\": {\"CostCenter\": \"42\"}}`

        __ https://docs.us-phoenix-1.oraclecloud.com/Content/General/Concepts/resourcetags.htm


        :return: The defined_tags of this CreateStreamDetails.
        :rtype: dict(str, dict(str, object))
        """
        return self._defined_tags

    @defined_tags.setter
    def defined_tags(self, defined_tags):
        """
        Sets the defined_tags of this CreateStreamDetails.
        Defined tags for this resource. Each key is predefined and scoped to a namespace. For more information, see `Resource Tags`__.

        Example: `{\"Operations\": {\"CostCenter\": \"42\"}}`

        __ https://docs.us-phoenix-1.oraclecloud.com/Content/General/Concepts/resourcetags.htm


        :param defined_tags: The defined_tags of this CreateStreamDetails.
        :type: dict(str, dict(str, object))
        """
        self._defined_tags = defined_tags

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
