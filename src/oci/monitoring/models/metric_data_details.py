# coding: utf-8
# Copyright (c) 2016, 2019, Oracle and/or its affiliates. All rights reserved.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class MetricDataDetails(object):
    """
    A metric object containing raw metric data points to be posted to the Monitoring service.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new MetricDataDetails object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param namespace:
            The value to assign to the namespace property of this MetricDataDetails.
        :type namespace: str

        :param compartment_id:
            The value to assign to the compartment_id property of this MetricDataDetails.
        :type compartment_id: str

        :param name:
            The value to assign to the name property of this MetricDataDetails.
        :type name: str

        :param dimensions:
            The value to assign to the dimensions property of this MetricDataDetails.
        :type dimensions: dict(str, str)

        :param metadata:
            The value to assign to the metadata property of this MetricDataDetails.
        :type metadata: dict(str, str)

        :param datapoints:
            The value to assign to the datapoints property of this MetricDataDetails.
        :type datapoints: list[Datapoint]

        """
        self.swagger_types = {
            'namespace': 'str',
            'compartment_id': 'str',
            'name': 'str',
            'dimensions': 'dict(str, str)',
            'metadata': 'dict(str, str)',
            'datapoints': 'list[Datapoint]'
        }

        self.attribute_map = {
            'namespace': 'namespace',
            'compartment_id': 'compartmentId',
            'name': 'name',
            'dimensions': 'dimensions',
            'metadata': 'metadata',
            'datapoints': 'datapoints'
        }

        self._namespace = None
        self._compartment_id = None
        self._name = None
        self._dimensions = None
        self._metadata = None
        self._datapoints = None

    @property
    def namespace(self):
        """
        **[Required]** Gets the namespace of this MetricDataDetails.
        The source service or application emitting the metric.

        A valid namespace value starts with an alphabetical character and includes only alphanumeric characters and underscores. The \"oci_\" prefix is reserved.
        Avoid entering confidential information.

        Example: `my_namespace`


        :return: The namespace of this MetricDataDetails.
        :rtype: str
        """
        return self._namespace

    @namespace.setter
    def namespace(self, namespace):
        """
        Sets the namespace of this MetricDataDetails.
        The source service or application emitting the metric.

        A valid namespace value starts with an alphabetical character and includes only alphanumeric characters and underscores. The \"oci_\" prefix is reserved.
        Avoid entering confidential information.

        Example: `my_namespace`


        :param namespace: The namespace of this MetricDataDetails.
        :type: str
        """
        self._namespace = namespace

    @property
    def compartment_id(self):
        """
        **[Required]** Gets the compartment_id of this MetricDataDetails.
        The `OCID`__ of the compartment to use for metrics.

        __ https://docs.us-phoenix-1.oraclecloud.com/iaas/Content/General/Concepts/identifiers.htm


        :return: The compartment_id of this MetricDataDetails.
        :rtype: str
        """
        return self._compartment_id

    @compartment_id.setter
    def compartment_id(self, compartment_id):
        """
        Sets the compartment_id of this MetricDataDetails.
        The `OCID`__ of the compartment to use for metrics.

        __ https://docs.us-phoenix-1.oraclecloud.com/iaas/Content/General/Concepts/identifiers.htm


        :param compartment_id: The compartment_id of this MetricDataDetails.
        :type: str
        """
        self._compartment_id = compartment_id

    @property
    def name(self):
        """
        **[Required]** Gets the name of this MetricDataDetails.
        The name of the metric.

        A valid name value starts with an alphabetical character and includes only alphanumeric characters, dots, underscores, hyphens, and dollar signs.
        Avoid entering confidential information.

        Example: `my_app.success_rate`


        :return: The name of this MetricDataDetails.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this MetricDataDetails.
        The name of the metric.

        A valid name value starts with an alphabetical character and includes only alphanumeric characters, dots, underscores, hyphens, and dollar signs.
        Avoid entering confidential information.

        Example: `my_app.success_rate`


        :param name: The name of this MetricDataDetails.
        :type: str
        """
        self._name = name

    @property
    def dimensions(self):
        """
        Gets the dimensions of this MetricDataDetails.
        Qualifiers provided in a metric definition. Available dimensions vary by metric namespace.

        Each dimension takes the form of a key-value pair. A valid dimension key includes only printable ASCII, excluding periods (.) and spaces. A valid dimension value includes only Unicode characters.
        Empty strings are not allowed for keys or values. Avoid entering confidential information.

        Example: `\"resourceId\": \"ocid1.instance.region1.phx.exampleuniqueID\"`


        :return: The dimensions of this MetricDataDetails.
        :rtype: dict(str, str)
        """
        return self._dimensions

    @dimensions.setter
    def dimensions(self, dimensions):
        """
        Sets the dimensions of this MetricDataDetails.
        Qualifiers provided in a metric definition. Available dimensions vary by metric namespace.

        Each dimension takes the form of a key-value pair. A valid dimension key includes only printable ASCII, excluding periods (.) and spaces. A valid dimension value includes only Unicode characters.
        Empty strings are not allowed for keys or values. Avoid entering confidential information.

        Example: `\"resourceId\": \"ocid1.instance.region1.phx.exampleuniqueID\"`


        :param dimensions: The dimensions of this MetricDataDetails.
        :type: dict(str, str)
        """
        self._dimensions = dimensions

    @property
    def metadata(self):
        """
        Gets the metadata of this MetricDataDetails.
        Properties describing metrics. These are not part of the unique fields identifying the metric.

        Example: `\"unit\": \"bytes\"`


        :return: The metadata of this MetricDataDetails.
        :rtype: dict(str, str)
        """
        return self._metadata

    @metadata.setter
    def metadata(self, metadata):
        """
        Sets the metadata of this MetricDataDetails.
        Properties describing metrics. These are not part of the unique fields identifying the metric.

        Example: `\"unit\": \"bytes\"`


        :param metadata: The metadata of this MetricDataDetails.
        :type: dict(str, str)
        """
        self._metadata = metadata

    @property
    def datapoints(self):
        """
        **[Required]** Gets the datapoints of this MetricDataDetails.
        A list of metric values with timestamps. At least one data point is required per call.


        :return: The datapoints of this MetricDataDetails.
        :rtype: list[Datapoint]
        """
        return self._datapoints

    @datapoints.setter
    def datapoints(self, datapoints):
        """
        Sets the datapoints of this MetricDataDetails.
        A list of metric values with timestamps. At least one data point is required per call.


        :param datapoints: The datapoints of this MetricDataDetails.
        :type: list[Datapoint]
        """
        self._datapoints = datapoints

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
