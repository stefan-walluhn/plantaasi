from machine import Timer

from plantaasi.bootstrap.config import config
from plantaasi.bootstrap.setup import Setup


def run():
    setup = Setup(config)
    setup()

    waterings = setup.waterings

    Timer(0).init(
        period=60000,
        mode=Timer.PERIODIC,
        callback=lambda t: [watering.run() for watering in waterings]
    )


if __name__ == '__main__':
    run()
