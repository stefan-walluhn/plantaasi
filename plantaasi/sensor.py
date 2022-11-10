import time

from machine import ADC
from machine import time_pulse_us


class Sensor:
    def read(self):
        raise NotImplementedError


class SideEffectSensor(Sensor):
    def __init__(self, sensor, side_effect):
        self.sensor = sensor
        self.side_effect = side_effect

    def read(self):
        reading = self.sensor.read()

        self.side_effect(reading)

        return reading


class MoistureSensor(Sensor):
    READ_CYCLES = 8
    MAX_REF = 1048576

    def __init__(self, pin, uv_high, uv_low):
        # uv value to percental value mapping is calculated by using a linear
        # function. Instead of processing the whole mapping on every read, we
        # can pre-process the params of the linear function instead
        # (y = mx + n)
        self._m = MoistureSensor.MAX_REF / (uv_high - uv_low)
        self._n = (uv_low * MoistureSensor.MAX_REF) / (uv_low - uv_high)

        self.adc = ADC(pin)
        self.adc.atten(ADC.ATTN_11DB)
        self.adc.width(ADC.WIDTH_10BIT)

    def _read_uvs(self, cycles):
        for _ in range(cycles):
            time.sleep_ms(1)
            yield self.adc.read_uv()

    def _read_uv(self):
        return (
            sum(self._read_uvs(MoistureSensor.READ_CYCLES))
            // MoistureSensor.READ_CYCLES
        )

    def read(self):
        return int(
            (self._m * self._read_uv() + self._n) * 100
            / MoistureSensor.MAX_REF
        )


class SR04T(Sensor):
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
