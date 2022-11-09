import machine
import esp32

from plantaasi.bootstrap.config import config
from plantaasi.bootstrap.plant import Plant


def run():
    plant = Plant(config)
    plant.setup()

    for watering in plant.waterings:
        watering.run()

    machine.deepsleep(60000)


def rescue():
    import network
    import webrepl

    ap = network.WLAN(network.AP_IF)
    ap.config(ssid='plantaasi')

    webrepl.start(password='plantaasi', port=8765)


if __name__ == '__main__':
    rescue_pin = machine.Pin(12, machine.Pin.IN, machine.Pin.PULL_UP)
    esp32.wake_on_ext0(rescue_pin, esp32.WAKEUP_ALL_LOW)

    if machine.wake_reason() is not machine.EXT0_WAKE:
        run()

    rescue()
