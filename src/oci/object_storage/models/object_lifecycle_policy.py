# coding: utf-8
# Copyright (c) 2016, 2019, Oracle and/or its affiliates. All rights reserved.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class ObjectLifecyclePolicy(object):
    """
    The collection of lifecycle policy rules that together form the object lifecycle policy of a given bucket.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new ObjectLifecyclePolicy object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param time_created:
            The value to assign to the time_created property of this ObjectLifecyclePolicy.
        :type time_created: datetime

        :param items:
            The value to assign to the items property of this ObjectLifecyclePolicy.
        :type items: list[ObjectLifecycleRule]

        """
        self.swagger_types = {
            'time_created': 'datetime',
            'items': 'list[ObjectLifecycleRule]'
        }

        self.attribute_map = {
            'time_created': 'timeCreated',
            'items': 'items'
        }

        self._time_created = None
        self._items = None

    @property
    def time_created(self):
        """
        Gets the time_created of this ObjectLifecyclePolicy.
        The date and time the object lifecycle policy was created, as described in
        `RFC 3339`__, section 14.29.

        __ https://tools.ietf.org/rfc/rfc3339


        :return: The time_created of this ObjectLifecyclePolicy.
        :rtype: datetime
        """
        return self._time_created

    @time_created.setter
    def time_created(self, time_created):
        """
        Sets the time_created of this ObjectLifecyclePolicy.
        The date and time the object lifecycle policy was created, as described in
        `RFC 3339`__, section 14.29.

        __ https://tools.ietf.org/rfc/rfc3339


        :param time_created: The time_created of this ObjectLifecyclePolicy.
        :type: datetime
        """
        self._time_created = time_created

    @property
    def items(self):
        """
        Gets the items of this ObjectLifecyclePolicy.
        The live lifecycle policy on the bucket.

        For an example of this value, see the
        `PutObjectLifecyclePolicy API documentation`__.

        __ https://docs.us-phoenix-1.oraclecloud.com/iaas/api/#/en/objectstorage/20160918/ObjectLifecyclePolicy/PutObjectLifecyclePolicy


        :return: The items of this ObjectLifecyclePolicy.
        :rtype: list[ObjectLifecycleRule]
        """
        return self._items

    @items.setter
    def items(self, items):
        """
        Sets the items of this ObjectLifecyclePolicy.
        The live lifecycle policy on the bucket.

        For an example of this value, see the
        `PutObjectLifecyclePolicy API documentation`__.

        __ https://docs.us-phoenix-1.oraclecloud.com/iaas/api/#/en/objectstorage/20160918/ObjectLifecyclePolicy/PutObjectLifecyclePolicy


        :param items: The items of this ObjectLifecyclePolicy.
        :type: list[ObjectLifecycleRule]
        """
        self._items = items

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
