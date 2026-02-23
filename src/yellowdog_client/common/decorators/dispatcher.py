from threading import Thread
from typing import Callable, Any


def dispatch_async(fn: Callable[..., Any]) -> Callable[..., Any]:
    def dispatch(*args: Any, **kwargs: Any) -> None:
        thread = Thread(target=fn, args=args, kwargs=kwargs)
        thread.start()
    return dispatch
