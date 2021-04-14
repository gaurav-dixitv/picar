from picar.libezblock import * 
from picar.picar import PiCar


def speed_test(car):
    car.forward(70)
    delay(1000)

    car.stop()
    delay(1000)

    car.backward(70)
    delay(1000)

    car.stop()
    delay(1000)


def head_test(car):
    car.set_angle(30)
    delay(1000)

    car.set_angle(-30)
    delay(1000)

    car.set_angle(0)
    delay(1000)




car = PiCar()

speed_test(car)
head_test(car)

