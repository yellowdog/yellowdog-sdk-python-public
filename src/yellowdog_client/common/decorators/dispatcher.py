from threading import Thread
from typing import Callable


def dispatch_async(fn: Callable) -> Callable:
    def dispatch(*args, **kwargs):
        thread = Thread(target=fn, args=args, kwargs=kwargs)
        thread.start()
    return dispatch
