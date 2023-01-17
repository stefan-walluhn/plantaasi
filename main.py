import machine
import esp32


RUN_EVERY_MINUTES = 10
RESCUE_PIN = 12


def run():
    from plantaasi import bootstrap, config

    plant = bootstrap.setup(config.load_config())
    plant.run()


def rescue():
    import network
    import webrepl

    ap = network.WLAN(network.AP_IF)
    ap.config(essid='plantaasi', max_clients=3)
    ap.active(True)

    webrepl.start(password='plantaasi', port=8765)


if __name__ == '__main__':
    rescue_pin = machine.Pin(RESCUE_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
    esp32.wake_on_ext0(rescue_pin, esp32.WAKEUP_ALL_LOW)

    if machine.wake_reason() is not machine.EXT0_WAKE:
        machine.WDT(timeout=RUN_EVERY_MINUTES*50000)
        run()
        machine.deepsleep(RUN_EVERY_MINUTES*60000)

    rescue()
