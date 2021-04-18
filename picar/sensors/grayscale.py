
from picar.libezblock import *
from picar.constants import *
import numpy as np
from enum import IntEnum
from typing import List

SensorOutput = List[int]


class Sensor:
    def __init__(self, adc_channels) -> None:
        self.channels = [ADC(channel) for channel in adc_channels]

    def read(self) -> SensorOutput:
        return [adc.read() for adc in self.channels]


class Polarity(IntEnum):
    Dark = -1
    Light = +1


class Interpreter:

    def __init__(self,
                 sensitivity: float = 1e-0,
                 polarity: Polarity = Polarity.Dark) -> None:

        self.sensitivity = sensitivity
        self.polarity = polarity

    def process(self, sensor_values: SensorOutput) -> float:

        # caluclate difference
        mid = len(sensor_values) // 2
        delta = np.array(sensor_values[:mid+1]) - \
            np.array(sensor_values[mid:]) * self.polarity

        delta[mid:] *= -1    # change the direction of the right half

        # return clipped value
        return np.clip(np.mean(delta) * self.sensitivity, -1, 1)


class Controller:

    def __init__(self, scale: float = 1.0) -> None:
        self.scale = scale

    # apply grayscale processed out -> angle transformation
    def steer(self, grayscale_out) -> float:
        return self.scale * grayscale_out
