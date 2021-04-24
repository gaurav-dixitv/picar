import threading
from collections import defaultdict
import copy


class AsyncBus:
    def __init__(self) -> None:
        self._message = defaultdict(set)
        self._lock = threading.Lock()

    # concurrent access for reading
    # assuming your message can be serialized.
    def read(self) -> dict:
        self._lock.acquire()
        message = copy.deepcopy(self._message)
        self._lock.release()
        return message

    # write mutex
    def write(self, value) -> None:
        self._lock.acquire()
        self._message.update(value)
        self._lock.release()
