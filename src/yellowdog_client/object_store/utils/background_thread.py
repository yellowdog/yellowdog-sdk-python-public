from typing import Callable
from threading import Thread


class BackgroundThread(object):
    _thread = None

    def __init__(self, target):
        # type: (Callable) -> None
        self._thread = Thread(target=target)
        self._thread.daemon = True

    def is_alive(self):
        # type: () -> bool
        return self._thread.is_alive()

    def start(self):
        # type: () -> None
        self._thread.start()

    def join(self):
        # type: () -> None
        self._thread.join()
