import time

from machine import Pin, Timer

from plantaasi.grafana import Grafana, Metric, Metrics
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


def init_metrics(sensors_config):
    metrics = []

    for sensor_config in sensors_config:
        sensor = MoistureSensor(Pin(sensor_config['pin']),
                                sensor_config['raw_hight'],
                                sensor_config['raw_low'])
        metrics.append(
            Metric('.'.join([sensor_config['metric'], 'perc']), sensor.read))
        metrics.append(
            Metric('.'.join([sensor_config['metric'], 'raw']),
                   sensor.read_raw_u16)
        )

    return Metrics(metrics)


def run():
    init_wifi(config['wifi']['essid'], config['wifi']['password'])
    init_time()

    metrics = init_metrics(config['sensors'])

    grafana = Grafana(config['grafana']['metrics_url'],
                      config['grafana']['user'],
                      config['grafana']['api_key'])

    Timer(0).init(period=60000, mode=Timer.PERIODIC,
                  callback=lambda t: grafana.push(list(metrics())))


if __name__ == '__main__':
    run()
