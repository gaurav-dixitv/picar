
from picar.libezblock import *
from picar.constants import *
import numpy as np
from enum import IntEnum
from typing import List
from picar.threading.async_bus import AsyncBus
from picar.threading.connect import Connect


SensorOutput = List[int]


class Sensor:
    def __init__(self, adc_channels, bus: AsyncBus) -> None:
        self.channels = [ADC(channel) for channel in adc_channels]
        self.bus = bus
        self.signals = Connect()

    def read(self, write=False) -> SensorOutput:

        # return [adc.read() for adc in self.channels]
        # instead of retuning, the sensor writes to a bus now
        sensor_values = [adc.read() for adc in self.channels]

        if write:
            self.bus.write({
                'adc': sensor_values
            })
        # emit signal "adc_update"
        self.signals.emit("adc_update")

        # slots connected to this signal can now update their values
        # safely with Sensor.signals.on("adc_update")
        print("Grayscale::Sensor::read() sensor read complete.")
        return sensor_values


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

    def __init__(self, bus: AsyncBus, car, scale: float = 1.0, *args, **kwargs) -> None:
        self.scale = scale
        self.bus = bus
        self.car = car
        self.interpreter = Interpreter(*args, **kwargs)

    def update(self):
        # new values availabel in the bus
        # read
        values = self.bus.read()['adc']
        # transform them
        values = self.interpreter.process(values)
        # steer
        self.steer(values)
        # log
        print("Grayscale::Controller::update() updated steering angle.")

    # apply grayscale processed out -> angle transformation
    def steer(self, grayscale_out) -> float:
        print("Grayscale::Controller::steer() steering.")
        self.car.set_angle(self.scale * grayscale_out)

    
