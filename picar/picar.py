import atexit
from .motorcontroller import MotorController

class PiCar:
    def __init__(self) -> None:
        self.motor = MotorController()
        atexit.register(self.__dint__)

    def __dint__(self) -> None:
        self.stop()
        self.set_angle(0)

    def set_speed(self, speed):
        self.motor.set_motor_speed(1, speed)
        self.motor.set_motor_speed(2, speed)

    def backward(self, speed = 80, calibrate = False, angle = 0):

        # if calibrate:
        #     self.motor.set_direction_calibration(2 if angle > 0 else 1, angle)
        
        retrograde_motor = 2 if angle > 0 else 1
        normal_motor = 1 if angle > 0 else 2

        if angle == 0:
            self.set_speed(speed)
        else:
            self.motor.set_motor_speed(retrograde_motor, abs(angle / 90.0) * speed)
            self.motor.set_motor_speed(normal_motor, speed)


    def forward(self, speed = 80, calibrate = False, angle = 0):

        # if calibrate:
        #     self.motor.set_direction_calibration(2 if angle > 0 else 1, angle)
        
        retrograde_motor = 2 if angle > 0 else 1
        normal_motor = 1 if angle > 0 else 2

        if angle == 0:
            self.set_speed(speed * -1)
        else:
            self.motor.set_motor_speed(retrograde_motor, abs(angle / 90.0) * speed * -1)
            self.motor.set_motor_speed(normal_motor, speed * -1)
        
    def set_angle(self, angle):
        self.motor.set_servo_angle(angle)
    
    def stop(self):
        self.motor.set_motor_speed(1, 0)
        self.motor.set_motor_speed(2, 0)