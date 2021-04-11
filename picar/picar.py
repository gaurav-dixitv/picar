import atexit
from .motorcontroller import MotorController

class PiCar:
    def __init__(self) -> None:
        self.motor = MotorController()
        atexit.register(self.__dint__)

    def __dint__(self) -> None:
        self.stop()

    def set_speed(self, speed):
        self.motor.set_motor_speed(1, speed)
        self.motor.set_motor_speed(2, speed)

    def backward(self, speed = 80, calibrate = False, angle = 0):

        self.set_speed(speed)

        if calibrate:
            self.motor.set_direction_calibration(2 if angle > 0 else 1, angle)
        
        self.motor.set_motor_speed(2 if angle > 0 else 1, abs((angle / 90.0) * speed))


    def forward(self, speed = 80, calibrate = False, angle = 0):

        self.set_speed(speed * -1)

        if calibrate:
            self.motor.set_direction_calibration(2 if angle > 0 else 1, angle)

        self.motor.set_motor_speed(2 if angle > 0 else 1, abs((angle / 90.0) * speed))

    def stop(self):
        self.motor.set_motor_speed(1, 0)
        self.motor.set_motor_speed(2, 0)