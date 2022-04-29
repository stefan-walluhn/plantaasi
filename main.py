import time

from machine import Pin, Timer

from plantaasi.grafana import Metric, Grafana
from plantaasi.moisture_sensor import MoistureSensor

from config import config


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
    ntptime.settime()


def run():
    init_wifi(config['wifi']['essid'], config['wifi']['password'])
    init_time()

    metric = Metric('test.moisture')

    grafana = Grafana(config['grafana']['metrics_url'],
                      config['grafana']['user'],
                      config['grafana']['api_key'])

    sensor = MoistureSensor(Pin(34), 17320, 41728)

    Timer(0).init(period=60000, mode=Timer.PERIODIC,
                  callback=lambda t: grafana.push([metric(sensor.read())]))


if __name__ == '__main__':
    run()
