
class PiResolution:
    def __init__(self) -> None:
        self.width = self.height = 64


class PiCamera:
    def __init__(self) -> None:
        self.resolution = PiResolution()

    def capture(self, buffer, format):
        pass
