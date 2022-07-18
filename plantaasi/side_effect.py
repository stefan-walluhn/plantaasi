class GrafanaMetric:
    def __init__(self, grafana, metric):
        self.grafana = grafana
        self.metric = metric

    def push_metric(self, value):
        self.grafana.push([self.metric(value)])
