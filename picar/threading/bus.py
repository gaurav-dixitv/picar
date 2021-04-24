import threading
from collections import defaultdict
import copy


class ThreadBus:
    def __init__(self) -> None:
        self._message = defaultdict(set)
        self._count = 0
        self._read_lock = threading.Lock()
        self._write_lock = threading.Lock()

        # queue is empty. lock reading
        self._read_lock.acquire()

    def length(self):
        return self._count

    # concurrent access for reading
    # assuming your message can be serialized.
    def read(self) -> dict:
        # stop further reads
        self._read_lock.acquire()
        message = copy.deepcopy(self._message)
        self._count -= 1
        # allow writes now
        self._write_lock.release()
        return message

    # write mutex
    def write(self, value) -> None:
        # stop further writes
        self._write_lock.acquire()
        self._message.update(value)
        self._count += 1
        # allow reads now
        self._read_lock.release()
