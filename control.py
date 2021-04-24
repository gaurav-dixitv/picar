
import sys
from picar.sim_ezblock.adc import test
from picar.libezblock import *
from picar.picar import PiCar
import picar.sensors.grayscale as Grayscale
import picar.sensors.camera as Camera

from threading import Event
from picar.threading.async_bus import AsyncBus
from picar.threading.bus import ThreadBus

import concurrent.futures
import time


def test_grayscale():
    """
    Test control loop with the grayscale sensor
    uses async signals & slots
    """

    car = PiCar()

    gray_bus = AsyncBus()
    sensor = Grayscale.Sensor(['A0', 'A1', 'A2'], gray_bus)
    controller = Grayscale.Controller(gray_bus, car)

    # connect the Grayscale::adc_update signal to the controller::update() slot
    @sensor.signals.on("adc_update")
    def adc_update():
        controller.update(car)

    # read from sensor 10 times
    tick = 0
    while tick < 10:
        sensor.read()
        tick += 1


def test_camera():
    """
    Test control loop with the on-board camera
    uses thread pool
    """

    car = PiCar()

    camera_sensor = Camera.Sensor()
    camera_controller = Camera.Controller(car)

    camera_bus = ThreadBus()
    event = Event()

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(camera_sensor.read, camera_bus, event)
        executor.submit(camera_controller.update, camera_bus, event)

        time.sleep(0.1)
        event.set()


if __name__ == '__main__':

    print("\ntesting async signals/slots with the grayscale sensor.")
    test_grayscale()

    print("\ntesting mutex read/write with the camera sensor.")
    test_camera()
