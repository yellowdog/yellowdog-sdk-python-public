from dataclasses import dataclass
from datetime import timedelta
from typing import ClassVar


@dataclass
class RetryProperties:
    """Defines properties that control services client retry behaviour"""
    DEFAULT_MAX_ATTEMPTS: ClassVar[int] = 3
    """The default maximum number of retries (3)"""
    DEFAULT_INITIAL_RETRY_INTERVAL: ClassVar[timedelta] = timedelta(seconds=10)
    """The default initial retry interval (10 seconds)"""
    DEFAULT_MAX_RETRY_INTERVAL: ClassVar[timedelta] = timedelta(minutes=1)
    """The default maximum retry interval (1 minute)"""
    maxAttempts: int = 3
    """
    The maximum number of retries after the initial request fails.
    A request is sent at most maxAttempts + 1 times before retries are exhausted.
    """

    initialInterval: timedelta = timedelta(seconds=10)
    """
    The initial interval before the first retry attempt.
    With Full Jitter applied, the actual interval of the first retry is anywhere between 0 and this value.
    Subsequent retry intervals grow exponentially.
    """

    maxInterval: timedelta = timedelta(minutes=1)
    """The maximum interval between retry attempts."""
