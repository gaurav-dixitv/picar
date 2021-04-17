from .sensor import *
import numpy as np


class Interpreter:

    def __init__(self,
                 sensitivity: float = 1e-0,
                 polarity: Polarity = Polarity.Dark,
                 threshold: float = None) -> None:

        self.sensitivity = sensitivity
        self.polarity = polarity
        self.threshold = threshold if threshold else self.sensitivity * 1500

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
