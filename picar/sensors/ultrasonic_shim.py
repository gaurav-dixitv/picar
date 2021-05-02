
from picar.libezblock import *
from picar.constants import *


class UltrsonicShim:
    """
    Shim to transparently pass calls to ezblocks/ultrasonic
    """

    def __init__(self,
                 car,
                 pin1: Pin,
                 pin2: Pin,
                 threshold) -> None:

        self.car = car
        self.pin1 = pin1
        self.pin2 = pin2
        self.threshold = threshold

    def read(self):
        print("UltrsonicShim::read() fetching values.")
        return Ultrasonic(self.pin1, self.pin2).read()

    def process(self, sensor_value):
        if sensor_value < self.threshold:
            return True
        return False

    def control(self, processed_value):
        """
        stop if we go beyond threshold
        otherwise continue
        """
        print("UltrsonicShim::control() updating car state.")
        if processed_value:
            self.car.stop()
