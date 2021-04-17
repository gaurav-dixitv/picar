
from picar.libezblock import *  # import ezblock
from picar.constants import *
from enum import IntEnum
from typing import List

SensorOutput = List[int]
class Polarity(IntEnum):
    Dark = -1
    Light = +1


class Sensor:
    def __init__(self, adc_channels) -> None:
        self.channels = [ADC(channel) for channel in adc_channels]

    def read(self) -> SensorOutput:
        return [adc.read() for adc in self.channels]
