import logging
import time

from usyslog import SyslogHandler

from plantaasi.bootstrap.builder import WateringBuilder
from plantaasi.grafana import Grafana
from plantaasi.utils import connect_wifi


log = logging.getLogger()


class Setup:
    watering_builder = WateringBuilder()

    def __init__(self, config):
        self.config = config
        self._waterings = None

    @property
    def waterings(self):
        assert self._waterings, "waterings need to be set up first"

        return self._waterings

    def setup_logging(self):
        if 'logging' not in self.config:
            return

        if 'loglevel' in self.config['logging']:
            logging.basicConfig(
                level=getattr(logging, self.config['logging']['loglevel'])
            )

        if 'syslog' in self.config['logging']:
            log.addHandler(SyslogHandler(**self.config['logging']['syslog']))

    def setup_wifi(self):
        log.info("setup wifi")

        connect_wifi(self.config['wifi']['essid'],
                     self.config['wifi']['password'])

    def setup_time(self):
        log.info("setup time")

        import ntptime

        while True:
            try:
                ntptime.settime()
                return
            except OSError:
                time.sleep(1)

    def setup_grafana(self):
        log.info("setup Grafana")

        Grafana().login(**self.config['grafana'])

    def setup_waterings(self):
        log.info("setup waterings")

        for watering_config in self.config['waterings']:
            yield self.watering_builder(**watering_config)

    def __call__(self):
        self.setup_logging()
        self.setup_wifi()
        self.setup_time()
        self.setup_grafana()
        self._waterings = list(self.setup_waterings())
