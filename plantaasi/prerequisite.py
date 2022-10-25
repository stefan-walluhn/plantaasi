import logging
import time


log = logging.getLogger(__name__)


class Prerequisite:
    def _fulfilled(self):
        raise NotImplementedError

    def fulfilled(self):
        ff = self._fulfilled()
        log.debug("%s %s fulfilled", self, "is" if ff else "is not")
        return ff


class Prerequisites(Prerequisite):
    def __init__(self, *prerequisites):
        self.prerequisites = prerequisites

    def _each_fulfilled(self):
        for prerequisite in self.prerequisites:
            yield prerequisite.fulfilled()

    def _fulfilled(self):
        # use list() to drain generator and trigger all side effects
        return False not in list(self._each_fulfilled())


class MoisturePrerequisite(Prerequisite):
    def __init__(self, sensor, threshold=30):
        self.sensor = sensor
        self.threshold = threshold

    def _fulfilled(self):
        return self.threshold > self.sensor.read()


class TimePrerequisite(Prerequisite):
    def _fulfilled(self):
        return time.localtime()[3] not in range(5, 19)
