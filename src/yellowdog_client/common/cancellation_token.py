from threading import Event, Lock
from typing import Callable, List


class CancellationToken:
    def __init__(self) -> None:
        self._cancelled = Event()
        self._callbacks: List[Callable[[], None]] = []
        self._lock = Lock()

    @property
    def cancelled(self) -> bool:
        return self._cancelled.is_set()

    def cancel(self) -> None:
        with self._lock:
            if self._cancelled.is_set():
                return
            self._cancelled.set()
            callbacks = self._callbacks
            self._callbacks = []
        for callback in callbacks:
            callback()

    def on_cancel(self, callback: Callable[[], None]) -> None:
        with self._lock:
            if not self._cancelled.is_set():
                self._callbacks.append(callback)
                return
        callback()
