import os
from pynetgear import Netgear

from prometheus_client import start_http_server
from prometheus_client import Counter, Gauge
from prometheus_client.registry import REGISTRY
from prometheus_client.metrics_core import CounterMetricFamily

class InternetStats(object):
  def __init__(self, registry=REGISTRY):
    self.netgear = Netgear(
      host = os.environ.get("NETGEAR_EXPORTER_HOST", None),
      password = os.environ.get("NETGEAR_EXPORTER_ADMIN_PASSWORD", None)
    )
    if registry:
      registry.register(self)

  def collect(self):
    traffic = self.netgear.get_traffic_meter()
    traffic_metric = CounterMetricFamily("traffic_meter", "traffic counters", labels=["direction"])
    traffic_metric.add_metric(["upload"], traffic['NewTodayUpload'])
    traffic_metric.add_metric(["download"], traffic['NewTodayDownload'])
    return [traffic_metric]

stats = InternetStats()

start_http_server(9192)

import time
while True:
  time.sleep(300)
