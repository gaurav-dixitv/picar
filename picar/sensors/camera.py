
from numpy.lib.type_check import imag
from picar.libezblock import *
import numpy as np
from .grayscale import Interpreter as GrayscaleInterpreter

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
        reference: https://towardsdatascience.com/deeppicar-part-4-lane-following-via-opencv-737dd9e47c96
        
        The reference already shows how to navigate within two lanes
        Let's see how well we can do with a heuristic instead!

        Heuristic
        1. Mask for blue (assuming blue tape)
        2. Apply blur + thresholding to capture dominant blobs
        3. Borrow the subtractive filtering from the grayscale sensor
            to compute which side is "brigher"
        4. Move in the direction to reduce the brighter side
        5. ...
        6. profit ?
        '''

        '''
        assuming blue waypoints,
        hsv blue range: 180 - 260
        cv2 blue range: 180/2 - 260/2 -> 90 - 130
        '''
        mask = cv2.inRange(
            cv2.cvtColor(image, cv2.COLOR_BGR2HSV),
            np.array([90, 0, 0]),
            np.array([130, 255, 255]))

        # using the value channel from the hsv image
        value = cv2.medianBlur(mask, 5)
        # Apply gaussian thresholding
        threshold = cv2.adaptiveThreshold(
            value,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY, 11, 2)

        # lanes only on the ground?
        image = self._roi(threshold)

        # flip row x columns!
        image = cv2.flip(image, 0)

        # process using grayscale detector
        processor = GrayscaleInterpreter()
        cumulative_direction = 0
        for row in image:
            cumulative_direction += processor.process(np.append(row, 0))

        if cumulative_direction > 0:
            return 1.0
        elif cumulative_direction < 0:
            return -1.0

        return 0.0


class Controller:

    def __init__(self, scale: float = 1.0) -> None:
        self.scale = scale

    # apply camera processed out -> angle transformation
    def steer(self, camera_out) -> float:
        return self.scale * camera_out
