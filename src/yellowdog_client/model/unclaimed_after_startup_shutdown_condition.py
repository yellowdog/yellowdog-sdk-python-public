from dataclasses import dataclass, field
from datetime import timedelta

from .worker_pool_shutdown_condition import WorkerPoolShutdownCondition


@dataclass
class UnclaimedAfterStartupShutdownCondition(WorkerPoolShutdownCondition):
    """Specifies that a worker pool should be automatically shut down if no workers have been claimed for the specified duration following worker pool startup."""
    type: str = field(default="co.yellowdog.platform.model.UnclaimedAfterStartupShutdownCondition", init=False)
    delay: timedelta
    """The duration to wait after the startup of the worker pool."""
