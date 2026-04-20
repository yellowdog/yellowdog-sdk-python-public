import random
from datetime import timedelta
from itertools import takewhile
import inspect
from typing import Any

from urllib3.util.retry import Retry

class FullJitterRetry(Retry):
    """
    Implementation of :class:`Retry` that implements the "Full Jitter" algorithm described by AWS <a href="https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/">Exponential Backoff And Jitter</a>.

    The maximum period between each subsequent retry increases exponentially.
    The actual period with full jitter will be anywhere between 0 and the maximum period.
    This approach should provide the best compromise between overall time to completion and load on the server.

    If the server sends a ``Retry-After`` header, the header will take precedence, unless `respect_retry_after_header` is `False`.
    See :meth:`sleep` for more information, but be aware backoff factor is ignored by :class:`FullJitterRetry` because it uses  `retry_initial_interval` instead.
    """

    def __init__(self, retry_max_interval: timedelta, retry_initial_interval: timedelta, **kwargs: Any):
        """
        Initialises a :class:`FullJitterRetry` instance.

        :param retry_max_interval: The upper bound on the computed backoff sleep time. The exponentially
            growing sleep window is capped at this value.
        :param retry_initial_interval: The initial interval used for the exponential backoff calculation.
            Also used as the ``backoff_factor`` passed to the parent :class:`Retry` class when that
            parameter is supported.
        :param kwargs: Additional keyword arguments forwarded to :class:`urllib3.util.retry.Retry`.
            ``backoff_factor``, ``backoff_max``, and ``backoff_jitter`` are set as defaults when the
            installed version of urllib3 supports them, providing a belt-and-braces fallback in case
            :meth:`get_backoff_time` is not called by the underlying library.
        """

        # Set the underlying Retry backoff_factor, backoff_jitter backoff_max to mitigate the chance of our overridden get_backoff_time() not being used
        # This is a belt and braces approach, because we do not have full control of which urllib3 is being used
        retry_parameters = inspect.signature(Retry).parameters
        if 'backoff_factor' in retry_parameters: kwargs.setdefault('backoff_factor', retry_initial_interval.total_seconds())
        if 'backoff_max'    in retry_parameters: kwargs.setdefault('backoff_max', retry_max_interval.total_seconds())
        if 'backoff_jitter' in retry_parameters: kwargs.setdefault('backoff_jitter', 0.5)
        super().__init__(**kwargs)
        self.retry_max_interval = retry_max_interval
        self.retry_initial_interval = retry_initial_interval

    def new(self, **kwargs: Any) -> "FullJitterRetry":
        kwargs.setdefault("retry_max_interval", self.retry_max_interval)
        kwargs.setdefault("retry_initial_interval", self.retry_initial_interval)
        return super().new(**kwargs)

    # Overrides the parent get_backoff_time ensuring we use FullJitter
    def get_backoff_time(self) -> float:
        """
        Calculates how long to sleep in seconds before retrying.
        Uses the _Full Jitter_ approach described by https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/

        :rtype: float
        """

        # return early if initial interval is 0 or negative
        if self.retry_initial_interval <= timedelta(0):
            return 0

        # We want to consider only the last consecutive errors sequence (Ignore redirects).
        consecutive_errors_len = len(
            list(
                takewhile(lambda x: x.redirect_location is None, reversed(self.history))
            )
        )
        if consecutive_errors_len <= 0:
            return 0

        # calculate the maximum length of time to sleep
        # exponentially increasing with each retry, remembering that x^0 always equals 1 where x is greater than 0
        max_sleep: float = min(
            self.retry_max_interval.total_seconds(),
            self.retry_initial_interval.total_seconds() * (2 ** (consecutive_errors_len - 1))
        )
        # multiply by a number between 0 and 1 to add full jitter
        # random.random() is 0 (inclusive) to 1 (exclusive) so it will never reach the maximum period
        # But a Python float is 2^53, so it's negligibly close to 1
        return random.random() * max_sleep

