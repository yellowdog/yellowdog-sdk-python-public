from typing import Callable
from threading import Lock


class SynchronizedPredicatedRunner(object):
    __sync_lock: Lock = None
    __predicate: Callable[[], bool] = None

    def __init__(self, predicate: Callable[[], bool]) -> None:
        self.__sync_lock = Lock()
        self.__predicate = predicate

    def run(self, runnable: Callable[[], None]) -> None:
        with self.__sync_lock:
            if self.__predicate():
                runnable()
