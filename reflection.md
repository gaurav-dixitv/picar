

<!-- PROJECT LOGO -->
<br />
<p align="center">
  <h3 align="center">picar -  motor commands</h3>
  <p align="center">
    an offline motor interface for the picar-x
    <br />
    <a href="https://github.com/gaurav-dixitv/picar/blob/main/README.md"><strong>repository readme »</strong></a>
    <br />
    <br />
    rob 521, week 2 - gaurav dixit
  </p>
</p>

<!-- TABLE OF CONTENTS -->
## Table of Contents

- [Table of Contents](#table-of-contents)
- [1/2 review](#12-review)
- [3.a lessons from motor task](#3a-lessons-from-motor-task)
- [3.b opportunities to improve](#3b-opportunities-to-improve)
- [Usage](#usage)


<!-- ABOUT THE PROJECT -->
## 1/2 review

I haven't received a review / code for review yet. As mentioned in the announcements, I will re-upload the reviews file independently.

<!-- GETTING STARTED -->
## 3.a lessons from motor task
1. Software calibration is hard - My kit did not have the correct pair of servo screws and arms. I verified this with a fellow classmate. I filed down the servo arms and used some M4 screws instead. This meant my direction (and pan) servos are a bit wonky. This effect is especially amplified when the car is mobile. Tweaking angle offsets in the code to make up for this error was daunting. 

2. 




## 3.b opportunities to improve

1. Use async/await architecture. Instead of `sleep()` and `delay()` calls with arbitrary pauses, an async await architecture would allow for cleaner serial execution.

For instance, 
```py
__reset_mcu__()
time.sleep(0.01)

sensor.reset()
```
would become:
```py
await __reset_mcu__()
sensor.reset()
```

2. raspberry pi network interface - I noticed many of my peers struggling to either get the pi to stay connected or just generally behave when connected to a wifi network.

Those not particularly comfortable with config files and/or linux would also probably enjoy a cli tool to interactively write the wpa_supplicant file. 
All debian distributions (including the raspbian we are using) include the program `wpa_cli`. It is an interactive command line tool that asks the user the SSID and password for the network and uses sane defaults for everything else (if skipped by the user).


Some of the sunfounder example programs try to connect to a hardcoded SSID. For some students, this led to the supplicant misbehaving and their pi got locked out of the network. The only solution was to write the `wpa_supplicant` file in the boot partition again. All of this can be avoided by directly writing the supplicant config file at `/etc/wpa_supplicant/wpa_supplicant.conf`.


Although the wpa supplicant is an excellent tool to quickly connect (especially for embedded devices), once a device is on the network, it is often a good idea to use a slightly more advanced network manager. Usually when I setup a new install, I start with the supplicant and then move on to using NetworkManger once I am online [NetworkManger on ArchWiki](https://wiki.archlinux.org/index.php/NetworkManager). The NetworkManger provides a clean ncurses based cli ui for scanning wired/wireless connections and connecting to new networks.

Setting up the NetworkManager is fairly straightforward:

* Install packages
```sh
sudo apt update && sudo apt install network-manager
```

* Configure the dhcp deamon to ignore wlan0. Add below line to `/etc/dhcpcd.conf`, 
```sh
denyinterfaces wlan0
```

* Configure NetworkManager to assume dhcp duties. Add to the file `/etc/NetworkManager/NetworkManager.conf`, 
```sh
[main]
plugins=ifupdown,keyfile
dhcp=internal

[ifupdown]
managed=true
```

* Restart
```sh
sudo reboot
```


3. Developing remotely - My linked github repository provides ssh configuration for `tramp` that can be used with emacs/vi to seamlessly connect and develop directly over ssh to the pi. The vscode remote-ssh plugin also allows developing on desktop seamlessly. 


4. The `sim_ezblocks` folder should be structured like a pip package (with a `__init__.py`). This will cleanly interface with `ezblocks` or `sim_ezblocks` depending on weather the code is run on the host or pi.

The repository then follows this structure loosely:
```
picar
│   README.md
│   .gitignore
|   LICENSE
|   garage.py    
│
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
│   
└───tests
    │   speed.py
    │   direction.py
    |   ...

```

<!-- USAGE EXAMPLES -->
## Usage

1. Using the ezblocks library: snippet from `picar/garage.py`
```py
from picar.libezblock import * 
from picar.picar import PiCar

car = PiCar()
car.forward(80)
delay(500)
car.backward(20)
delay(100)
car.stop()

car.forward(calibrate=False, angle=30)

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