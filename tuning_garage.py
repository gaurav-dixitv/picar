from picar.libezblock import * 
from picar.picar import PiCar

car = PiCar


car.forward(80)
delay(1000)
car.backward(20)
delay(2000)
car.stop()

car.forward(calibrate=False, angle=30)
