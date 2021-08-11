from dataclasses import dataclass
from datetime import timedelta


@dataclass
class RetryProperties:
    """Defines properties that control services client retry behaviour"""
    maxAttempts: int = 3
    """
    Set the number of attempts before retries are exhausted.
    Includes the initial attempt before the retries begin.
    """

    initialInterval: timedelta = timedelta(seconds=5)
    """The initial interval before the first retry attempt."""
    maxInterval: timedelta = timedelta(minutes=1)
    """The maximum interval between retry attempts."""
