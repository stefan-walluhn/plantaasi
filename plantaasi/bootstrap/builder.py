import logging

from machine import Pin, Signal

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
        log.debug("create PumpTrigger on pin %d", pin)

        return PumpTrigger(
            Pump(Signal(Pin(pin, mode=Pin.OPEN_DRAIN, value=1), invert=True)),
            duration
        )


class WateringBuilder:
    _builders = {'moisture': MoisturePrerequisiteBuilder(),
                 'time': TimePrerequisiteBuilder(),
                 'pump': PumpTriggerBuilder()}

    def _build_members(self, config):
        for k, v in config.items():
            yield self._builders[k](**v)

    def __call__(self, prerequisites, triggers):
        log.debug("create watering")

        return Watering(
            Prerequisites(*self._build_members(prerequisites)),
            Triggers(*self._build_members(triggers))
        )
