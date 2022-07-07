import time


class Pump:
    def __init__(self, pin, duration):
        self.pin = pin
        self.duration = duration

    def trigger(self):
        self.pin.on()
        time.sleep(self.duration)
        self.pin.off()
