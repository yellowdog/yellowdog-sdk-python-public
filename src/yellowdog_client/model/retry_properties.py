from dataclasses import dataclass
from datetime import timedelta
from typing import ClassVar


@dataclass
class RetryProperties:
    """Defines properties that control services client retry behaviour"""
    DEFAULT_MAX_ATTEMPTS: ClassVar[int] = 3
    """The default max attempt count (3)"""
    DEFAULT_INITIAL_RETRY_INTERVAL: ClassVar[timedelta] = timedelta(seconds=5)
    """The default initial retry interval (5 seconds)"""
    DEFAULT_MAX_RETRY_INTERVAL: ClassVar[timedelta] = timedelta(minutes=1)
    """The default maximum retry interval (1 minute)"""
    maxAttempts: int = 3
    """
    Set the number of attempts before retries are exhausted.
    Includes the initial attempt before the retries begin.
    """

    initialInterval: timedelta = timedelta(seconds=5)
    """The initial interval before the first retry attempt."""
    maxInterval: timedelta = timedelta(minutes=1)
    """The maximum interval between retry attempts."""
