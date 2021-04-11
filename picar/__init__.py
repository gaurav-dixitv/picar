import time
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
    time.sleep(0.01)