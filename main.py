import machine

from plantaasi.bootstrap.config import config
from plantaasi.bootstrap.plant import Plant


def run():
    plant = Plant(config)
    plant.setup()

    for watering in plant.waterings:
        watering.run()

    machine.deepsleep(60000)


if __name__ == '__main__':
    if machine.wake_reason() is not machine.EXT0_WAKE:
        run()
