<!-- PROJECT LOGO -->
<br />
<p align="center">
  <h3 align="center">picar</h3>
  <p align="center">
    an offline motor interface for the picar-x
    <br />
    <a href="https://github.com/gaurav-dixitv/picar/blob/main/README.md"><strong>repository readme »</strong></a>
    <br />
    <br />
  </p>
</p>

<!-- TABLE OF CONTENTS -->
## Table of Contents

- [Table of Contents](#table-of-contents)
- [setup](#setup)
- [navigating the repository](#navigating-the-repository)
- [usage](#usage)


<!-- ABOUT THE PROJECT -->
## setup
* clone 
```sh
git clone https://github.com/gaurav-dixitv/picar
```

* setup a virtual environment, 
```sh
mkdir venv && python3 -m venv venv/
```

* source the virtual environment, 
```sh
. venv/bin/activate
```

* run all tests,
```sh
python3 tuning_garage.py
```

## navigating the repository

The `sim_ezblocks` folder is structred like pip package. This will cleanly interface with `ezblocks` or `sim_ezblocks` depending on weather the code is run on the host or pi.

The repository follows this structure loosely:
```
picar
│   README.md
│   .gitignore
|   LICENSE
|   tuning_garage.py
│   control.py
|
└───picar
│   │   __init__.py
│   │   libezblocks.py
│   │   motor.py
│   │   car.py
│   │   constants.py
│   │   ...
│   │
│   └───sim_ezblock
│       │   __init__.py
│       │   servo.py
│       │   ...
|       |
│   └───sim_camera
│       │   __init__.py
│       │   picamera.py
│       │   ...
|
└───tests
    │   speed.py
    │   direction.py
    |   ...

```

<!-- USAGE EXAMPLES -->
## usage

1. Using the ezblocks library: snippet from `picar/garage.py`
```py
from picar.libezblock import * 
from picar.picar import PiCar

car = PiCar()
car.forward(80)
car.backward(20)

car.forward(calibrate=False, angle=30)

car.stop()

```

2.  A snippet from `picar/picar/libezblocks.py` that chooses the right ezblocks package at run time:
```py
try:
    import ezblock as __ezb  # import private members namespaceded as __ezb
    from ezblock import *
except ImportError:
    print("This computer does not appear to be a PiCar-X system. \n\
        /opt/ezblock is not present.\n\
        Shadowing hardware calls with stubs")
    import picar.sim_ezblock as __ezb  # import private members namespaceded as __ezb
    from picar.sim_ezblock import *
finally:
    __ezb.__reset_mcu__()
```

3.  Snippet from `picar/picar/car.py` that creates a car using the motor primitives:
```py
import atexit
from .motorcontroller import MotorController

class PiCar:
    def __init__(self) -> None:
        self.motor = MotorController()
        atexit.register(self.__dint__)

    def __dint__(self) -> None:
        self.stop()

    def backward(self, speed = 80, calibrate = False, angle = 0):

        self.set_speed(speed)

        if calibrate:
            self.motor.set_direction_calibration(
                    2 if angle > 0 else 1, angle
                )

...
```