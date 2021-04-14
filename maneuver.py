#!/usr/bin/python3

from picar.libezblock import *
from picar.picar import PiCar


class Maneuver:
    def __init__(self) -> None:
        # create car
        self.car = PiCar()

    def reset(self):
        self.car.stop()
        self.car.set_angle(0)

    def move_in(self, dir):
        if dir == "forward":
            self.car.forward(75)
        elif dir == "backward":
            self.car.backward(75)
        elif dir == "forward left":
            self.car.set_angle(-30)
            self.car.forward(75, angle=-30)
        elif dir == "forward right":
            self.car.set_angle(30)
            self.car.forward(75, angle=30)
        elif dir == "backward left":
            self.car.set_angle(-30)
            self.car.backward(75, angle=-30)
        elif dir == "backward right":
            self.car.set_angle(30)
            self.car.backward(75, angle=30)
        elif dir == 'stop':
            self.car.stop()

    def park(self, dir):
        if dir == "left":
            self.car.forward(75, angle=0)
            self.car.set_angle(-30)
            delay(1000)
            self.car.set_angle(30)
            delay(1000)
            self.car.stop()

        elif dir == "right":
            self.car.forward(75, angle=0)
            self.car.set_angle(30)
            delay(1000)
            self.car.set_angle(-30)
            delay(1000)
            self.car.stop()
        else:
            self.car.stop()
            print("Re-enter the action...: ")

    def k_turn(self, dir):
        if dir == "left":
            self.car.set_angle(-30)
            self.car.forward(75)
            delay(1000)
            self.car.stop()

            self.car.set_angle(30)
            self.car.backward(50)
            delay(1000)
            self.car.stop()

            self.car.set_angle(-20)
            self.car.forward(75)
            delay(1000)
            self.car.set_angle(0)
            delay(1000)
            self.stop()

        elif dir == "right":

            self.car.set_angle(30)
            self.car.forward(75)
            delay(1000)
            self.car.stop()

            self.car.set_angle(-30)
            self.car.backward(50)
            delay(1000)
            self.car.stop()

            self.car.set_angle(20)
            self.car.forward(75)
            delay(1000)
            self.car.set_angle(0)
            delay(1000)
            self.stop()


if __name__ == "__main__":

    maneuver = Maneuver()
    while True:
        usr_input = int(input(
            "Choose maneuver: \n1] move in direction \n2] park in direction \n3] k-turn \n4] stop \n5] exit \n"))
        maneuver.reset()

        if usr_input == 1:
            dir_in = input("direction to move: ")
            maneuver.move_in(dir_in)

        elif usr_input == 2:
            dir_in = input("Park left or right:")
            maneuver.park(dir_in)

        elif usr_input == 3:
            dir_in = input("k-turn left or right: ")
            maneuver.k_turn(dir_in)

        elif usr_input == 4:
            maneuver.reset()

        elif usr_input == 5:
            maneuver.reset()
            break

        else:
            print("Choose an action...: ")
