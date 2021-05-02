
from picar.libezblock import *
from picar.picar import PiCar
import picar.sensors.grayscale as Grayscale
import picar.sensors.ultrasonic_shim as Ultrasonic

from picar.utilities.rossros import Bus, Producer, ConsumerProducer, Consumer, runConcurrently


if __name__ == '__main__':

    print("\ntesting grayscale sensor. Using ultrasonic sensor for breaks.")

    # test car
    car = PiCar()

    # grayscale sensor, interpreter and controller
    sensor = Grayscale.Sensor(['A0', 'A1', 'A2'], None)
    interpreter = Grayscale.Interpreter()
    controller = Grayscale.Controller(None, car)

    # grayscale in / out buses
    gray_in_bus = Bus(initial_message=[0, 0, 0], name="gray_in_bus")
    gray_out_bus = Bus(initial_message=0.0, name="gray_out_bus")

    # grayscale controls
    grayscale_producer = Producer(sensor.read,
                                  output_busses=gray_in_bus,
                                  delay=0.5,
                                  name="grayscale_producer")
    # process every other input -
    grayscale_control = ConsumerProducer(interpreter.process,
                                         input_busses=gray_in_bus,
                                         output_busses=gray_out_bus,
                                         delay=1.0,
                                         name="grayscale_control")
    grayscale_consumer = Consumer(controller.steer,
                                  input_busses=gray_out_bus,
                                  delay=1.0,
                                  name="grayscale_consumer")

    # ultrasonic shim with read/interpret/control methods
    ultrasonic = Ultrasonic.UltrsonicShim(car,
                                          Pin('D0'),
                                          Pin('D1'),
                                          75)   # threshold
    # ultrasonic in / out
    ultrasonic_in_bus = Bus(initial_message=100, name="ultrasonic_in_bus")
    ultrasonic_out_bus = Bus(initial_message=False, name="ultrasonic_out_bus")

    ultrasonic_producer = Producer(ultrasonic.read,
                                   output_busses=ultrasonic_in_bus,
                                   delay=0.25,
                                   name="ultrasonic_producer")

    # process every other input, slightly higher polling rate
    # adjust polling rate based on torque/speed characteristics
    ultrasonic_control = ConsumerProducer(ultrasonic.process,
                                          input_busses=ultrasonic_in_bus,
                                          output_busses=ultrasonic_out_bus,
                                          delay=0.5,
                                          name="ultrasonic_control")
    ultrasonic_consumer = Consumer(ultrasonic.control,
                                   input_busses=ultrasonic_out_bus,
                                   delay=0.5,
                                   name="ultrasonic_consumer")

    # start both control loops
    runConcurrently([
        # grayscale
        grayscale_producer,
        grayscale_control,
        grayscale_consumer,

        # brakes
        ultrasonic_producer,
        ultrasonic_control,
        ultrasonic_consumer]
    )
