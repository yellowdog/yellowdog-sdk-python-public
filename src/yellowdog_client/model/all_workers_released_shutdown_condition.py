from dataclasses import dataclass, field
from datetime import timedelta

from .worker_pool_shutdown_condition import WorkerPoolShutdownCondition


@dataclass
class AllWorkersReleasedShutdownCondition(WorkerPoolShutdownCondition):
    """Specifies that a worker pool should be automatically shut down when all its workers have been released."""
    type: str = field(default="co.yellowdog.platform.model.AllWorkersReleasedShutdownCondition", init=False)
    delay: timedelta
    """The duration to wait after the last worker release before automatic shutdown."""
