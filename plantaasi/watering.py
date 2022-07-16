class Watering:
    def __init__(self, prerequisite, trigger):
        self.prerequisite = prerequisite
        self.trigger = trigger

    def run(self):
        if self.prerequisite.fulfilled():
            self.trigger()
