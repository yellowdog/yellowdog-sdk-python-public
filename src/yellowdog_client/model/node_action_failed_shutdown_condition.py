from dataclasses import dataclass, field
from datetime import timedelta

from .worker_pool_shutdown_condition import WorkerPoolShutdownCondition


@dataclass
class NodeActionFailedShutdownCondition(WorkerPoolShutdownCondition):
    """Specifies that a worker pool should be automatically shut down if a node configuration action has failed to be executed successfully."""
    type: str = field(default="co.yellowdog.platform.model.NodeActionFailedShutdownCondition", init=False)
    delay: timedelta
    """The duration to wait after the last node action failed."""
