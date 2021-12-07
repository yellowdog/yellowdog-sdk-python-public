from dataclasses import dataclass, field
from datetime import timedelta

from .worker_pool_shutdown_condition import WorkerPoolShutdownCondition


@dataclass
class AllNodesInactiveShutdownCondition(WorkerPoolShutdownCondition):
    """Specifies that a worker pool should be automatically shut down when all its nodes are inactive."""
    type: str = field(default="co.yellowdog.platform.model.AllNodesInactiveShutdownCondition", init=False)
    delay: timedelta
    """The time delay to wait after the last node is inactive before automatic shutdown."""
