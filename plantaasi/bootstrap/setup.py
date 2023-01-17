import logging

from lib.usyslog import SyslogHandler

from plantaasi.bootstrap.builder import WateringBuilder
from plantaasi.grafana import Grafana
from plantaasi.plant import Plant
from plantaasi.utils import connect_wifi, ntpdate


log = logging.getLogger(__name__)


def setup_wifi(config):
    log.info("setup wifi")

    try:
        connect_wifi(config['wifi']['essid'], config['wifi']['password'])
    except RuntimeError as e:
        log.error(e.value)


def setup_logging(config):
    if 'logging' not in config:
        return

    if 'loglevel' in config['logging']:
        logging.basicConfig(
            level=getattr(logging, config['logging']['loglevel'])
        )

    if 'syslog' in config['logging']:
        log.warning("switching to remote syslog handler")
        log.addHandler(SyslogHandler(**config['logging']['syslog']))


def setup_time():
    log.info("setup time")

    try:
        ntpdate()
    except RuntimeError as e:
        log.error(e.value)


def setup_grafana(config):
    log.info("setup Grafana")

    Grafana().login(**config['grafana'])


def setup_waterings(config):
    log.info("setup waterings")

    watering_builder = WateringBuilder()
    for watering_config in config['waterings']:
        yield watering_builder(**watering_config)


def setup_plant(config):
    log.info("setup plant")

    return Plant(*setup_waterings(config))


def setup(config):
    log.info("starting plant setup")

    setup_wifi(config)
    setup_logging(config)
    setup_time()
    setup_grafana(config)
    return setup_plant(config)
