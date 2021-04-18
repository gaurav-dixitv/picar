
from numpy.lib.type_check import imag
from picar.libezblock import *
import numpy as np

# check if you are on a raspberry, fallback to stubs otherwise
try:
    from picamera import PiCamera
except ImportError:
    print("ImportError: Unable to determine if this system is a Raspberry Pi.")
    from picar.sim_picamera.picamera import PiCamera    # use stubs
finally:
    import cv2
    import time

SensorOutput = np.array


class Sensor:
    def __init__(self) -> None:
        self.camera = PiCamera()
        # wait for automatic controls
        time.sleep(2)
        self.output = np.empty(
            (self.camera.resolution.height,
             self.camera.resolution.width, 3),
            dtype=np.uint8)

    def read(self) -> SensorOutput:
        self.camera.capture(self.output, "bgr")
        return self.output


class Interpreter:

    def __init__(self,
                 sensitivity: float = 1e-0) -> None:

        self.sensitivity = sensitivity

    def _roi(self, edges):
        height, width = edges.shape
        mask = np.zeros_like(edges)

        # values closer to the sensor
        polygon = np.array([[
            (0, height * 1 / 2),
            (width, height * 1 / 2),
            (width, height),
            (0, height),
        ]], np.int32)

        cv2.fillPoly(mask, polygon, 255)
        cropped_edges = cv2.bitwise_and(edges, mask)
        return cropped_edges

    def process(self, sensor_values: SensorOutput) -> float:

        image = sensor_values

        '''
        assuming blue waypoints,
        hsv blue range: 180 - 260
        cv2 blue range: 180/2 - 260/2 -> 90 - 130
        '''
        mask = cv2.inRange(
            cv2.cvtColor(image, cv2.COLOR_BGR2HSV),
            np.array([90, 0, 0]),
            np.array([130, 255, 255]))

        # convert to gray
        gray = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)

        # Apply gaussian tresholding
        treshold = cv2.adaptiveThreshold(
            gray,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY, 11, 2)

        cv2.imwrite("/tmp/treshold.png", treshold)

        # Canny edge detection
        # edges = cv2.Canny(mask, 200, 400)   # TODO check Canny.threshold[12]

        # lanes only on the ground?
        # image = self._roi(edges)



        return 0.0

        # caluclate difference
        mid = len(sensor_values) // 2
        delta = np.array(sensor_values[:mid+1]) - \
            np.array(sensor_values[mid:])

        delta[mid:] *= -1    # change the direction of the right half

        # return clipped value
        return np.clip(np.mean(delta) * self.sensitivity, -1, 1)


class Controller:

    def __init__(self, scale: float = 1.0) -> None:
        self.scale = scale

    # apply camera processed out -> angle transformation
    def steer(self, camera_out) -> float:
        return self.scale * camera_out
