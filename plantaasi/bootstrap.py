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
    def __call__(self, pin, raw_hight, raw_low, threshold):
        return MoisturePrerequisite(
            MoistureSensor(Pin(pin), raw_hight, raw_low),
            threshold=threshold
        )


class TimePrerequisiteBuilder:
    def __call__(self):
        return TimePrerequisite()


class PumpTriggerBuilder:
    def __call__(self, pin, duration):
        return PumpTrigger(
            Pump(Pin(pin, mode=Pin.OPEN_DRAIN, value=0)), duration
        )


class WateringBuilder:
    def __init__(self):
        self._builder = {'moisture': MoisturePrerequisiteBuilder(),
                         'time': TimePrerequisiteBuilder(),
                         'pump': PumpTriggerBuilder()}

    def get_wattering(self, watering_config):
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


def init_waterings(waterings_config):
    watering_builder = WateringBuilder()

    for watering_config in waterings_config:
        yield watering_builder.get_wattering(watering_config)
