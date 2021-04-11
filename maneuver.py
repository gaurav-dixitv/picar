#!/usr/bin/python3

from picar.libezblock import * 
from picar.picar import PiCar


class Maneuver:
    def __init__(self) -> None:
        # create car
        self.car = PiCar()

    def move_in(self, dir):
        if dir == "forward":
            self.car.forward(50)
        elif dir == "backward":
            self.car.backward(50) 
        elif dir == "forward left": 
            self.car.forward(50, angle=-30)
        elif dir == "forward right": 
            self.car.forward(50, angle=30)
        elif dir == "backward left":
            self.car.backward(50, angle=-30)
        elif dir == "backward right": 
            self.car.backward(50, angle=30)
        elif dir == 'stop':
            self.car.stop()

    def park(self, dir):
        if dir == "left":
            self.car.forward(50, angle=0)
            self.car.forward(50, angle=-30)
            delay(1000)
            self.car.forward(50, angle=30)
            delay(500)
            self.car.stop()
            self.car.forward(0, angle=-30)
        elif dir == "right":
            self.car.forward(50, angle=0)
            self.car.forward(50, angle=30)
            delay(1000)
            self.car.forward(50, angle=-30)
            delay(500)
            self.car.stop()
        else:
            self.car.stop()
            print("Re-enter the action...: ") 

    def k_turn(self, dir):
        if dir == "left":
            self.car.forward(50, angle=-30)
            delay(1000)
            self.car.stop()
            self.car.backward(50, angle=30)
            delay(1000)
            self.car.stop()
            self.car.forward(50, angle=-20)
            delay(1000)
            self.stop()

        elif dir == "left":
            self.car.forward(50, angle=30)
            delay(1000)
            self.car.stop()
            self.car.backward(50, angle=-30)
            delay(1000)
            self.car.stop()
            self.car.forward(50, angle=20)
            delay(1000)
            self.stop()


if __name__ == "__main__":

    maneuver = Maneuver()
    while True:
        usr_input = int(input("Choose an action: "))
        if usr_input == 1:
           dir_in = input("Choose a direction: ")
           maneuver.move_in(dir_in)

        elif usr_input == 2:
           dir_in = input("Choose left or right")
           maneuver.park(dir_in)
      
        elif usr_input == 3:
            dir_in = input("Choose left or right")
            maneuver.k_turn(dir_in)

        elif usr_input == 4:
            maneuver.car.stop()
            maneuver.car.set_speed(0)

        elif usr_input == 5:
            maneuver.car.stop()
            break

        else:
            print("Choose an action...: ") 
