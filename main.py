import machine

from plantaasi.bootstrap.config import config
from plantaasi.bootstrap.setup import Setup


def run():
    setup = Setup(config)
    setup()

    for watering in setup.waterings:
        watering.run()

    machine.deepsleep(60000)


if __name__ == '__main__':
    if machine.wake_reason() is not machine.EXT0_WAKE:
        run()
