from machine import ADC


class MoistureSensor:
    READ_CYCLE = 8
    MAX_REF = 32000  # arbitrary; use sensible value to utilize esp32 floats

    def __init__(self, pin, raw_high, raw_low):
        # raw value to percental value mapping is calculated by using a linear
        # function. Instead of processing the whole mapping on every read, we
        # can pre-process the params of the linear function instead
        # (y = mx + n)
        self.m = MoistureSensor.MAX_REF / (raw_high - raw_low)
        self.n = (raw_low * MoistureSensor.MAX_REF) / (raw_low - raw_high)

        self.adc = ADC(pin)
        self.adc.atten(ADC.ATTN_11DB)
        self.adc.width(ADC.WIDTH_10BIT)

    def _read_raw_u16(self):
        raw = 0
        for _ in range(MoistureSensor.READ_CYCLE):
            raw += self.adc.read_u16()

        return raw // MoistureSensor.READ_CYCLE

    def read(self):
        perc = (self.m * self._read_raw_u16() + self.n) / MoistureSensor.MAX_REF

        return int(perc * 100)
