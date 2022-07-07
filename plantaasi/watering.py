class Watering:
    def __init__(self, prerequisites, trigger):
        self.prerequisites = prerequisites
        self.trigger = trigger

    def run(self):
        if self.prerequisites.fulfilled():
            self.trigger()
