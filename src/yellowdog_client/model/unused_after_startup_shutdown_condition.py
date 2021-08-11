from dataclasses import dataclass, field
from datetime import timedelta

from .worker_pool_shutdown_condition import WorkerPoolShutdownCondition


@dataclass
class UnusedAfterStartupShutdownCondition(WorkerPoolShutdownCondition):
    """Specifies that a worker pool should be automatically shut down if it remains unused for the specified duration following worker pool startup."""
    type: str = field(default="co.yellowdog.platform.model.UnusedAfterStartupShutdownCondition", init=False)
    delay: timedelta
    """The duration to wait after the startup of the worker pool."""
