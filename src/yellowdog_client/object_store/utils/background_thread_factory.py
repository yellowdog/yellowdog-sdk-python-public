from typing import Callable

from .background_thread import BackgroundThread


class BackgroundThreadFactory(object):
    @staticmethod
    def new_thread(target: Callable) -> BackgroundThread:
        return BackgroundThread(target=target)
