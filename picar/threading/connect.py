from functools import wraps
from threading import Thread
from collections import defaultdict, Counter
from typing import Iterable, Callable, List, Dict, Any, Set, Union

# signals & slots
# reference: https://doc.qt.io/qt-5/signalsandslots.html


class Connect:

    __slots__ = ('_signals',)

    def __init__(self) -> None:
        """ Creates new Connect object. """
        self._signals = defaultdict(set)

    def on(self, signal: str) -> Callable:
        """ Decorator for connecting a slot to a specific signal.
        :param signal: Name of the signal to connect to.
        :type signal: str
        """

        def outer(func):
            self.add_signal(func, signal)

            @wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            return wrapper

        return outer

    def add_signal(self, func: Callable, signal: str) -> None:
        """ Adds a slot to a signal.
        :param signal: Name of the signal.
        :type signal: str
        """
        self._signals[signal].add(func)

    def emit(self, signal: str, *args, **kwargs) -> None:
        """ Emit an signal and run the connected slots.

        :param signal: Name of the signal.
        :type signal: str
        """
        threads = kwargs.pop('threads', None)

        if threads:

            signals = [
                Thread(target=f, args=args, kwargs=kwargs) for f in
                self._signal_funcs(signal)
            ]
            print("starting threads..", len(signals))
            for signal in signals:
                signal.start()

        else:
            for func in self._signal_funcs(signal):
                func(*args, **kwargs)

    def _signal_funcs(self, signal: str) -> Iterable[Callable]:
        """ Returns an Iterable of the slots connected to a signal.

        :param signal: Name of the signal.
        :type signal: str
        """
        for func in self._signals[signal]:
            yield func
