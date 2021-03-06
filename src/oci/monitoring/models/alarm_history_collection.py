# coding: utf-8
# Copyright (c) 2016, 2019, Oracle and/or its affiliates. All rights reserved.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class AlarmHistoryCollection(object):
    """
    The configuration details for retrieving alarm history.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new AlarmHistoryCollection object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param alarm_id:
            The value to assign to the alarm_id property of this AlarmHistoryCollection.
        :type alarm_id: str

        :param is_enabled:
            The value to assign to the is_enabled property of this AlarmHistoryCollection.
        :type is_enabled: bool

        :param entries:
            The value to assign to the entries property of this AlarmHistoryCollection.
        :type entries: list[AlarmHistoryEntry]

        """
        self.swagger_types = {
            'alarm_id': 'str',
            'is_enabled': 'bool',
            'entries': 'list[AlarmHistoryEntry]'
        }

        self.attribute_map = {
            'alarm_id': 'alarmId',
            'is_enabled': 'isEnabled',
            'entries': 'entries'
        }

        self._alarm_id = None
        self._is_enabled = None
        self._entries = None

    @property
    def alarm_id(self):
        """
        **[Required]** Gets the alarm_id of this AlarmHistoryCollection.
        The `OCID`__ of the alarm for which to retrieve history.

        __ https://docs.us-phoenix-1.oraclecloud.com/iaas/Content/General/Concepts/identifiers.htm


        :return: The alarm_id of this AlarmHistoryCollection.
        :rtype: str
        """
        return self._alarm_id

    @alarm_id.setter
    def alarm_id(self, alarm_id):
        """
        Sets the alarm_id of this AlarmHistoryCollection.
        The `OCID`__ of the alarm for which to retrieve history.

        __ https://docs.us-phoenix-1.oraclecloud.com/iaas/Content/General/Concepts/identifiers.htm


        :param alarm_id: The alarm_id of this AlarmHistoryCollection.
        :type: str
        """
        self._alarm_id = alarm_id

    @property
    def is_enabled(self):
        """
        **[Required]** Gets the is_enabled of this AlarmHistoryCollection.
        Whether the alarm is enabled.

        Example: `true`


        :return: The is_enabled of this AlarmHistoryCollection.
        :rtype: bool
        """
        return self._is_enabled

    @is_enabled.setter
    def is_enabled(self, is_enabled):
        """
        Sets the is_enabled of this AlarmHistoryCollection.
        Whether the alarm is enabled.

        Example: `true`


        :param is_enabled: The is_enabled of this AlarmHistoryCollection.
        :type: bool
        """
        self._is_enabled = is_enabled

    @property
    def entries(self):
        """
        **[Required]** Gets the entries of this AlarmHistoryCollection.
        The set of history entries retrieved for the alarm.


        :return: The entries of this AlarmHistoryCollection.
        :rtype: list[AlarmHistoryEntry]
        """
        return self._entries

    @entries.setter
    def entries(self, entries):
        """
        Sets the entries of this AlarmHistoryCollection.
        The set of history entries retrieved for the alarm.


        :param entries: The entries of this AlarmHistoryCollection.
        :type: list[AlarmHistoryEntry]
        """
        self._entries = entries

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
