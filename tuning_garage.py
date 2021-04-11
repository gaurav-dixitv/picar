from picar.libezblock import * 
from picar.picar import PiCar

car = PiCar()
car.forward(80)
delay(500)
car.backward(20)
delay(100)
car.stop()

car.forward(calibrate=False, angle=30)
