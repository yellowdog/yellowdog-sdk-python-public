from typing import Optional
import time
from threading import Lock

from cancel_token import CancellationToken


class ChunkTransferThrottle(object):
    @property
    def max_bytes_per_second(self):
        # type: () -> int
        return self._max_bytes_per_second

    @max_bytes_per_second.setter
    def max_bytes_per_second(self, value):
        # type: (int) -> None
        self._max_bytes_per_second = value
        self._max_bytes_per_period = self._throttle_period_seconds * value

    @staticmethod
    def _current_time_in_ms():
        # type: () -> float
        time_in_s = time.time()
        return time_in_s * 1000

    def __init__(self, throttle_period_sec):
        # type: (int) -> None
        self._throttle_period_seconds = throttle_period_sec                     # type: int
        self._throttle_period_ms = self._throttle_period_seconds * 1000         # type: int
        self._max_bytes_per_second = 0                                          # type: int
        self._max_bytes_per_period = 0                                          # type: int
        self._throttle_sync_lock = Lock()                                       # type: Lock
        self._bytes_transferred = 0                                             # type: int
        self._end_time = None                                                   # type: Optional[float]
        self._start_time = self._current_time_in_ms()                           # type: float

    def start(self):
        # type: () -> None
        self._end_time = None
        self._start_time = self._current_time_in_ms()

    def stop(self):
        # type: () -> None
        self._end_time = self._current_time_in_ms()

    def wait_for_transfer_bandwidth(self, chunk_size, cancellation_token):
        # type: (int, CancellationToken) -> None
        if self._max_bytes_per_second == 0:
            return
        while not cancellation_token.cancelled:
            with self._throttle_sync_lock:
                current_time = self._current_time_in_ms()
                elapsed = current_time - self._start_time
                if elapsed >= self._throttle_period_ms:
                    self._bytes_transferred = chunk_size
                    self._start_time = current_time
                    return
                if chunk_size + self._bytes_transferred <= self._max_bytes_per_second:
                    self._bytes_transferred += chunk_size
                    return
                sleep_ms = self._throttle_period_ms - elapsed
                sleep_s = sleep_ms / 1000
                time.sleep(sleep_s)
