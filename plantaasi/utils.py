import network
import ntptime
import time


class Singleton(object):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Singleton, cls).__new__(cls)

        return cls._instance


def connect_wifi(essid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        wlan.connect(essid, password)

        while not wlan.isconnected():
            time.sleep(1)


def ntpdate():
    for i in range(10):
        try:
            ntptime.settime()
            return
        except OSError:
            time.sleep(i ** 2)

    raise RuntimeError("unable to set time using ntp")
