import logging
import time

from machine import Pin

from plantaasi.grafana import Grafana, Metric
from plantaasi.prerequisite import (Prerequisites,
                                    MoisturePrerequisite,
                                    TimePrerequisite)
from plantaasi.pump import Pump
from plantaasi.sensor import MoistureSensor, SideEffectSensor
from plantaasi.side_effect import GrafanaMetric
from plantaasi.trigger import Triggers, PumpTrigger
from plantaasi.watering import Watering


log = logging.getLogger(__name__)


class MoisturePrerequisiteBuilder:
    def __call__(self, pin, raw_hight, raw_low, threshold, metric=None):
        sensor = MoistureSensor(Pin(pin), raw_hight, raw_low)
        if metric:
            grafana_metric = GrafanaMetric(Grafana(), Metric(metric))
            sensor = SideEffectSensor(sensor, grafana_metric.push_metric)

        log.debug("create MoisturePrerequisite using '%s' on pin %d",
                  sensor.__class__.__name__, pin)

        return MoisturePrerequisite(sensor, threshold=threshold)


class TimePrerequisiteBuilder:
    def __call__(self):
        log.debug("create TimePrerequisite")

        return TimePrerequisite()


class PumpTriggerBuilder:
    def __call__(self, pin, duration):
        log.debug("create PumpTriggerBuilder on pin %d", pin)

        return PumpTrigger(
            Pump(Pin(pin, mode=Pin.OPEN_DRAIN, value=0)), duration
        )


class WateringBuilder:
    def __init__(self):
        self._builder = {'moisture': MoisturePrerequisiteBuilder(),
                         'time': TimePrerequisiteBuilder(),
                         'pump': PumpTriggerBuilder()}

    def get_wattering(self, watering_config):
        log.debug("create watering")

        return Watering(
            Prerequisites(
                *self._build_members(watering_config['prerequisites'])
            ),
            Triggers(*self._build_members(watering_config['triggers']))
        )

    def _build_members(self, config):
        for k, v in config.items():
            yield self._builder[k](**v)


def init_wifi(essid, password):
    log.info("init wifi")

    import network

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        wlan.connect(essid, password)

        while not wlan.isconnected():
            time.sleep(1)


def init_time():
    log.info("init time")

    import ntptime

    while True:
        try:
            ntptime.settime()
            return
        except OSError:
            time.sleep(1)


def init_grafana(metrics_url, instance_id, api_key):
    log.info("init Grafana")

    Grafana().login(metrics_url, instance_id, api_key)


def init_waterings(waterings_config):
    log.info("init waterings")

    watering_builder = WateringBuilder()

    for watering_config in waterings_config:
        yield watering_builder.get_wattering(watering_config)
