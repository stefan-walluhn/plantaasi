import logging
import time


log = logging.getLogger()


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

    def _fulfilled(self):
        return False not in [p.fulfilled() for p in self.prerequisites]


class MoisturePrerequisite(Prerequisite):
    def __init__(self, sensor, threshold=30):
        self.sensor = sensor
        self.threshold = threshold

    def _fulfilled(self):
        return self.threshold > self.sensor.read()


class TimePrerequisite(Prerequisite):
    def _fulfilled(self):
        return time.localtime()[3] not in range(5, 19)
