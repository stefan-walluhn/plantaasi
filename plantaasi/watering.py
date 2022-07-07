class Watering:
    def __init__(self, prerequisites, pump):
        self.prerequisites = prerequisites
        self.pump = pump

    def run(self):
        if self.prerequisites.fulfilled():
            self.pump.trigger()
