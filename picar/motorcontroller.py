from .libezblock import *  # import ezblock
from .constants import *

class MotorController:
    def __init__(self) -> None:

        self.direction_pins = [Pin("D4"), Pin("D5")]
        self.speed_pins = [PWM("P13"), PWM("P12")]
        for pin in self.speed_pins:
            pin.period(Constants.PERIOD)
            pin.prescaler(Constants.PRESCALER)

        self.calibrated_speed = [1, -1]
        self.calibrated_direction =  [0, 0]
    
    def set_motor_speed(self, motor, speed):
        # index with 0
        motor -= 1
        # direction
        if speed >= 0:
            direction = 1 * self.calibrated_direction[motor]
        elif speed < 0:
            direction = -1 * self.calibrated_direction[motor]
        
        # speed
        speed = abs(speed)
        # offset caliberation
        speed = speed - self.calibrated_speed[motor]
        if direction < 0:
            self.direction_pins[motor].high()
            self.speed_pins[motor].pulse_width_percent(speed)
        else:
            self.direction_pins[motor].low()
            self.speed_pins[motor].pulse_width_percent(speed)

    def set_speed_calibration(self, value):
        self.calibrated_speed = [0, 0]
        if value < 0:
            self.calibrated_speed[1] = abs(value)
        else:
            self.calibrated_speed[0] = abs(value)

    def set_direction_calibration(self, motor, value):
        motor -= 1
        if value == 1:
            self.calibrated_direction[motor] = -1 * self.calibrated_direction[motor]
