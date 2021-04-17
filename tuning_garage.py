from picar.sensors.sensor import Sensor
from picar.libezblock import *
from picar.picar import PiCar
import picar.sensors.grayscale as Grayscale


def speed_test(car: PiCar) -> None:
    car.forward(70)
    delay(1000)

    car.stop()
    delay(1000)

    car.backward(70)
    delay(1000)

    car.stop()
    delay(1000)


def head_test(car: PiCar) -> None:
    car.set_angle(30)
    delay(1000)

    car.set_angle(-30)
    delay(1000)

    car.set_angle(0)
    delay(1000)


def sense_gray() -> None:
    sensor = Sensor(['A0', 'A1', 'A2'])
    interpreter = Grayscale.Interpreter()
    direction = interpreter.process(sensor.read())
    print("[Garage::sense_gray] move in direction: ", direction)


def control_gray(car: PiCar, ticks: int = 10) -> None:

    sensor = Sensor(['A0', 'A1', 'A2'])
    interpreter = Grayscale.Interpreter()
    controller = Grayscale.Controller()

    # reset car and set in motion
    car.reset()
    car.forward()

    # steer using gray sensor for `ticks` ticks
    tick = 0
    while tick < ticks:
        gray = interpreter.process(sensor.read())
        steering_angle = controller.steer(gray)
        car.set_angle(steering_angle)
        tick += 1

    # stop car
    car.reset()


car = PiCar()

speed_test(car)
head_test(car)

sense_gray()
control_gray(car)
