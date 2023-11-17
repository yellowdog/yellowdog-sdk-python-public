from threading import Lock
from concurrent.futures import Future

from cancel_token import CancellationToken


class CountdownEvent(object):
    def __init__(self, count: int) -> None:
        if count <= 0:
            raise ValueError(f"count must be greater than zero but was {count}")

        self._counter_lock = Lock()
        self.initial_count: int = count
        self._counter: int = count
        self._future_to_wait: Future = Future()
        self._future_to_wait.set_running_or_notify_cancel()

    @property
    def counter(self) -> int:
        with self._counter_lock:
            return self._counter

    @counter.setter
    def counter(self, value: int) -> None:
        with self._counter_lock:
            self._counter = value
            if self._counter == 0:
                self._future_to_wait.set_result(result=0)

    def wait(self, cancellation_token: CancellationToken) -> int:
        cancellation_token.on_cancel(callback=self._future_to_wait.cancel)
        return self._future_to_wait.result()



