import time
import urequests as requests


class Metric:
    TIME_OFFSET = 946684800

    def __init__(self, name, value_callback, interval=60):
        self.name = name
        self.value_callback = value_callback
        self.interval = interval

    def __call__(self):
        return dict(name=self.name,
                    value=self.value_callback(),
                    interval=self.interval,
                    time=time.time() + Metric.TIME_OFFSET)


class Grafana:
    def __init__(self, metrics_url, instance_id, api_key):
        self.metrics_url = metrics_url
        self.headers = {"Authorization": f"Bearer {instance_id}:{api_key}"}

    def push(self, metrics):
        response = requests.post(self.metrics_url,
                                 headers=self.headers, json=metrics)
        response.close()
