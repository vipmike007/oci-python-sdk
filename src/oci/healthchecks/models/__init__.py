# coding: utf-8
# Copyright (c) 2016, 2019, Oracle and/or its affiliates. All rights reserved.

from __future__ import absolute_import

from .connection import Connection
from .create_http_monitor_details import CreateHttpMonitorDetails
from .create_on_demand_http_probe_details import CreateOnDemandHttpProbeDetails
from .create_on_demand_ping_probe_details import CreateOnDemandPingProbeDetails
from .create_ping_monitor_details import CreatePingMonitorDetails
from .dns import DNS
from .geolocation import Geolocation
from .health_checks_vantage_point_summary import HealthChecksVantagePointSummary
from .http_monitor import HttpMonitor
from .http_monitor_summary import HttpMonitorSummary
from .http_probe import HttpProbe
from .http_probe_result_summary import HttpProbeResultSummary
from .ping_monitor import PingMonitor
from .ping_monitor_summary import PingMonitorSummary
from .ping_probe import PingProbe
from .ping_probe_result_summary import PingProbeResultSummary
from .routing import Routing
from .tcp_connection import TcpConnection
from .update_http_monitor_details import UpdateHttpMonitorDetails
from .update_ping_monitor_details import UpdatePingMonitorDetails

# Maps type names to classes for healthchecks services.
healthchecks_type_mapping = {
    "Connection": Connection,
    "CreateHttpMonitorDetails": CreateHttpMonitorDetails,
    "CreateOnDemandHttpProbeDetails": CreateOnDemandHttpProbeDetails,
    "CreateOnDemandPingProbeDetails": CreateOnDemandPingProbeDetails,
    "CreatePingMonitorDetails": CreatePingMonitorDetails,
    "DNS": DNS,
    "Geolocation": Geolocation,
    "HealthChecksVantagePointSummary": HealthChecksVantagePointSummary,
    "HttpMonitor": HttpMonitor,
    "HttpMonitorSummary": HttpMonitorSummary,
    "HttpProbe": HttpProbe,
    "HttpProbeResultSummary": HttpProbeResultSummary,
    "PingMonitor": PingMonitor,
    "PingMonitorSummary": PingMonitorSummary,
    "PingProbe": PingProbe,
    "PingProbeResultSummary": PingProbeResultSummary,
    "Routing": Routing,
    "TcpConnection": TcpConnection,
    "UpdateHttpMonitorDetails": UpdateHttpMonitorDetails,
    "UpdatePingMonitorDetails": UpdatePingMonitorDetails
}
