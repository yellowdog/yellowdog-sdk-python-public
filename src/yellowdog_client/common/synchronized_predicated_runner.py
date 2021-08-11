from typing import Callable
from threading import Lock


class SynchronizedPredicatedRunner(object):
    __sync_lock = None        # type: Lock
    __predicate = None        # type: Callable[[], bool]

    def __init__(self, predicate):
        # type: (Callable[[], bool]) -> None
        self.__sync_lock = Lock()
        self.__predicate = predicate

    def run(self, runnable):
        # type: (Callable[[], None]) -> None
        with self.__sync_lock:
            if self.__predicate():
                runnable()
