from threading import Lock
# noinspection PyCompatibility
from concurrent.futures import Future

from cancel_token import CancellationToken


class CountdownEvent(object):
    def __init__(self, count):
        # type: (int) -> None
        self._counter_lock = Lock()
        self.initial_count = count              # type: int
        self._counter = count                   # type: int
        self._future_to_wait = Future()         # type: Future
        self._future_to_wait.set_running_or_notify_cancel()

    @property
    def counter(self):
        # type: () -> int
        with self._counter_lock:
            return self._counter

    @counter.setter
    def counter(self, value):
        # type: (int) -> None
        with self._counter_lock:
            self._counter = value
            if self._counter == 0:
                self._future_to_wait.set_result(result=0)

    def wait(self, cancellation_token):
        # type: (CancellationToken) -> int
        cancellation_token.on_cancel(callback=self._future_to_wait.cancel)
        return self._future_to_wait.result()



