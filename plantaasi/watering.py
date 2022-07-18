import logging


log = logging.getLogger(__name__)


class Watering:
    def __init__(self, prerequisite, trigger):
        self.prerequisite = prerequisite
        self.trigger = trigger

    def run(self):
        log.info("running %s", self)

        if self.prerequisite.fulfilled():
            log.info("prerequisite for %s is fulfilled, triggering", self)
            self.trigger()
