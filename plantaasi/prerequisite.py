import time


class Prerequisite:
    def fulfilled(self):
        raise NotImplementedError


class Prerequisites(Prerequisite):
    def __init__(self, *prerequisites):
        self.prerequisites = prerequisites

    def _each_fulfilled(self):
        for prerequisite in self.prerequisites:
            yield prerequisite.fulfilled()

    def fulfilled(self):
        return False not in self._each_fulfilled()

        # Note to self: if we must cycle ALL fulfilled checks, we have to use
        # `list` to empty the generator! Otherwise this will return on first
        # hit:
        # return False not in list(self._each_fulfilled())


class MoisturePrerequisite(Prerequisite):
    def __init__(self, sensor, threshold=30):
        self.sensor = sensor
        self.threshold = threshold

    def fulfilled(self):
        return self.threshold < self.sensor.read()


class TimePrerequisite(Prerequisite):
    def fulfilled(self):
        return time.localtime()[3] not in range(6, 20)
