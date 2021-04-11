#!/usr/bin/env python3
from .i2c import I2C


class ADC(I2C):
    ADDR = 0x14

    def __init__(self, chn):
        super().__init__()
        if isinstance(chn, str):
            if chn.startswith("A"):
                chn = int(chn[1:])
            else:
                raise ValueError(
                    "ADC channel should be between [A0, A7], not {0}".format(chn))
        if chn < 0 or chn > 7:
            self._error('Incorrect channel range')
        chn = 7 - chn
        self.chn = chn | 0x10
        self.reg = 0x40 + self.chn

    def read(self):
        self._debug("Write 0x%02X to 0x%02X" % (self.chn, self.ADDR))
        self.send([self.chn, 0, 0], self.ADDR)

        self._debug("Read from 0x%02X" % (self.ADDR))
        value_h = self.recv(1, self.ADDR)[0]

        self._debug("Read from 0x%02X" % (self.ADDR))
        value_l = self.recv(1, self.ADDR)[0]

        value = (value_h << 8) + value_l
        self._debug("Read value: %s" % value)
        return value

    def read_voltage(self):
        return self.read*3.3/4095


def test():
    import time
    adc = ADC(0)
    while True:
        print(adc.read())
        time.sleep(1)


if __name__ == '__main__':
    test()
