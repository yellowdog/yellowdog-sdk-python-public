from typing import Callable
from threading import Thread


class BackgroundThread(object):
    _thread = None

    def __init__(self, target: Callable) -> None:
        self._thread = Thread(target=target)
        self._thread.daemon = True

    def is_alive(self) -> bool:
        return self._thread.is_alive()

    def start(self) -> None:
        self._thread.start()

    def join(self) -> None:
        self._thread.join()
