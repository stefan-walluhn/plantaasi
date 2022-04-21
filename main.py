import time

from config import config
from machine import Timer


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


def rand_metric(url, instance_id, api_key):
    import urequests as requests
    import random

    response = requests.post(
        url,
        headers={"Authorization": f"Bearer {instance_id}:{api_key}"},
        json=[{'name': 'test.esp32',
               'value': random.uniform(0.0, 100.0),
               'interval': 60,
               'time': time.time() + 946684800}]
    )
    response.close()


def run():
    init_wifi(config['wifi']['essid'], config['wifi']['password'])
    init_time()

    Timer(0).init(
        period=60000,
        mode=Timer.PERIODIC,
        callback=lambda t: rand_metric(config['grafana']['metrics_url'],
                                       config['grafana']['user'],
                                       config['grafana']['api_key'])
    )


if __name__ == '__main__':
    run()
