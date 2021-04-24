from numpy.lib.type_check import imag
from picar.libezblock import *
from picar.picar import PiCar
import picar.sensors.grayscale as Grayscale
import picar.sensors.camera as Camera


def test_speed(car: PiCar) -> None:
    car.forward(70)
    delay(1000)

    car.stop()
    delay(1000)

    car.backward(70)
    delay(1000)

    car.stop()
    delay(1000)


def test_head(car: PiCar) -> None:
    car.set_angle(30)
    delay(1000)

    car.set_angle(-30)
    delay(1000)

    car.set_angle(0)
    delay(1000)


car = PiCar()

test_speed(car)
test_head(car)


'''
deprecated

def test_steering(
        sensor,
        interpreter,
        controller,
        car: PiCar,
        ticks: int = 10) -> None:

    print(f"[Garage::test_steering] testing steering with {sensor}.")
    # reset car and set in motion
    car.reset()
    car.forward()

    # steer using sensor for `ticks` ticks
    tick = 0
    while tick < ticks:
        sensor_out = interpreter.process(sensor.read())
        steering_angle = controller.steer(sensor_out)
        car.set_angle(steering_angle)
        tick += 1

    # stop car
    car.reset()

test_gray()
test_steering(
    sensor=Grayscale.Sensor(['A0', 'A1', 'A2']),
    interpreter=Grayscale.Interpreter(),
    controller=Grayscale.Controller(),
    car=car
)

test_steering(
    sensor=Camera.Sensor(),
    interpreter=Camera.Interpreter(),
    controller=Camera.Controller(),
    car=car
)
'''
