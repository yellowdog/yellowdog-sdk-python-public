from typing import Optional
import time
from threading import Lock

from cancel_token import CancellationToken


class ChunkTransferThrottle(object):
    @property
    def max_bytes_per_second(self) -> int:
        return self._max_bytes_per_second

    @max_bytes_per_second.setter
    def max_bytes_per_second(self, value: int) -> None:
        self._max_bytes_per_second = value
        self._max_bytes_per_period = self._throttle_period_seconds * value

    @staticmethod
    def _current_time_in_ms() -> float:
        time_in_s = time.time()
        return time_in_s * 1000

    def __init__(self, throttle_period_sec: int) -> None:
        self._throttle_period_seconds: int = throttle_period_sec
        self._throttle_period_ms: int = self._throttle_period_seconds * 1000
        self._max_bytes_per_second: int = 0
        self._max_bytes_per_period: int = 0
        self._throttle_sync_lock: Lock = Lock()
        self._bytes_transferred: int = 0
        self._end_time: Optional[float] = None
        self._start_time: float = self._current_time_in_ms()

    def start(self) -> None:
        self._end_time = None
        self._start_time = self._current_time_in_ms()

    def stop(self) -> None:
        self._end_time = self._current_time_in_ms()

    def wait_for_transfer_bandwidth(self, chunk_size: int, cancellation_token: CancellationToken) -> None:
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
