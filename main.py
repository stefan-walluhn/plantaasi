from machine import Timer

from plantaasi.config import config
from plantaasi.bootstrap import (init_logging,
                                 init_wifi,
                                 init_time,
                                 init_grafana,
                                 init_waterings)


def run():
    init_logging(config.get('loglevel', 'INFO'))
    init_wifi(**config['wifi'])
    init_time()
    init_grafana(**config['grafana'])

    waterings = list(init_waterings(config['waterings']))

    Timer(0).init(
        period=60000,
        mode=Timer.PERIODIC,
        callback=lambda t: [watering.run() for watering in waterings]
    )


if __name__ == '__main__':
    run()
