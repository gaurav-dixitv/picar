timer = [
    {
        "arr": 0
    }
] * 4


class PWM():
    REG_CHN = 0x20
    REG_FRE = 0x30
    REG_PSC = 0x40
    REG_ARR = 0x44

    ADDR = 0x14

    CLOCK = 72000000

    def __init__(self, channel, debug="critical"):
        super().__init__()
        if isinstance(channel, str):
            if channel.startswith("P"):
                channel = int(channel[1:])
            else:
                raise ValueError(
                    "PWM channel should be between [P1, P14], not {0}".format(channel))

        self.debug = debug

    def i2c_write(self, reg, value):
        pass

    def freq(self, *freq):
        pass

    def prescaler(self, *prescaler):
        pass

    def period(self, *arr):
        pass

    def pulse_width(self, *pulse_width):
        pass

    def pulse_width_percent(self, *pulse_width_percent):
        pass


def test():
    pass


def test2():
    pass


if __name__ == '__main__':
    test2()
