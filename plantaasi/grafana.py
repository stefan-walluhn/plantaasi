import logging
import time
import urequests as requests


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


class Grafana(object):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Grafana, cls).__new__(cls)

        return cls._instance

    def login(self, metrics_url, instance_id, api_key):
        self.metrics_url = metrics_url
        self.headers = {"Authorization": f"Bearer {instance_id}:{api_key}"}

    def push(self, metrics):
        log.info("pushing grafana metrics")
        response = requests.post(self.metrics_url,
                                 headers=self.headers, json=metrics)
        response.close()
