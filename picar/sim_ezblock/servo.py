from .basic import _Basic_class


class Servo(_Basic_class):
    MAX_PW = 2500
    MIN_PW = 500
    _freq = 50

    def __init__(self, pwm):
        super().__init__()

    # angle ranges -90 to 90 degrees
    def angle(self, angle):
        pass


def test():
    pass


if __name__ == "__main__":
    test()
