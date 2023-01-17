import lib.urequests as requests
import logging
import time

from plantaasi.utils import Singleton


log = logging.getLogger(__name__)


class Metric:
    TIME_OFFSET = 946684800

    def __init__(self, name, interval=60):
        self.name = name
        self.interval = interval

    def __call__(self, value):
        log.debug("format metric '%s' using value %0.4f", self.name, value)

        return dict(name=self.name,
                    value=value,
                    interval=self.interval,
                    time=time.time() + Metric.TIME_OFFSET)


class Grafana(Singleton):
    def login(self, metrics_url, instance_id, api_key):
        self.metrics_url = metrics_url
        self.headers = {"Authorization": f"Bearer {instance_id}:{api_key}"}

    def push(self, metrics):
        log.debug("pushing grafana metrics")
        try:
            requests.post(
                self.metrics_url,
                headers=self.headers,
                json=metrics,
                timeout=20
            ).close()
        except OSError as e:
            log.exc(e, "error while pushing grafana metrics")
            return
