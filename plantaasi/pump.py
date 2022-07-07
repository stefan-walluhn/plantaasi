import time


class Pump:
    def __init__(self, pin):
        self.pin = pin

    def trigger(self, duration):
        self.pin.on()
        time.sleep(duration)
        self.pin.off()
