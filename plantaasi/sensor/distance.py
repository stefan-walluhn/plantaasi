import time
from machine import Pin, time_pulse_us


class SR04T:
    SONIC_SPEED = 343.2

    def __init__(self, trigger_pin, echo_pin):
        self.trigger_pin = trigger_pin
        self.echo_pin = echo_pin

    def _trigger(self):
        self.trigger_pin.on()
        time.sleep_us(10)
        self.trigger_pin.off()

    def _read_raw_us(self):
        self._trigger()

        return time_pulse_us(self.echo_pin, 1)

    def read(self):
        # raw / 1000000 * sonic speed / 2
        return self._read_raw_us() * SR04T.SONIC_SPEED / 2000000
