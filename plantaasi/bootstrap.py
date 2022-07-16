import time

from machine import Pin

from plantaasi.prerequisite import (Prerequisites,
                                    MoisturePrerequisite,
                                    TimePrerequisite)
from plantaasi.pump import Pump
from plantaasi.sensor import MoistureSensor
from plantaasi.trigger import Triggers, PumpTrigger
from plantaasi.watering import Watering


class MoisturePrerequisiteBuilder:
    def get_prerequisite(self, pin, raw_hight, raw_low, threshold):
        return MoisturePrerequisite(
            MoistureSensor(Pin(pin), raw_hight, raw_low),
            threshold=threshold
        )


class TimePrerequisiteBuilder:
    def get_prerequisite(self):
        return TimePrerequisite()


class PumpTriggerBuilder:
    def get_trigger(self, pin, duration):
        return PumpTrigger(Pump(Pin(pin, mode=Pin.OPEN_DRAIN, value=0)),
                           duration)


class WateringBuilder:
    def __init__(self):
        self._prerequisite_builder = {
            'moisture': MoisturePrerequisiteBuilder(),
            'time': TimePrerequisiteBuilder()
        }

        self._trigger_builder = {'pump': PumpTriggerBuilder()}

    def get_wattering(self, watering_config):
        return Watering(
            Prerequisites(
                *self._prerequisites(watering_config['prerequisites'])
            ),
            Triggers(*self._triggers(watering_config['triggers']))
        )

    def _prerequisites(self, prerequisites_config):
        for k, v in prerequisites_config.items():
            yield self._prerequisite_builder[k].get_prerequisite(**v)

    def _triggers(self, triggers_config):
        for k, v in triggers_config.items():
            yield self._trigger_builder[k].get_trigger(**v)


def init_wifi(essid, password):
    import network

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        wlan.connect(essid, password)

        while not wlan.isconnected():
            time.sleep(1)


def init_time():
    import ntptime
    while True:
        try:
            ntptime.settime()
            return
        except OSError:
            time.sleep(1)
