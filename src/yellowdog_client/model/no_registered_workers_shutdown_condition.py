from dataclasses import dataclass, field

from .worker_pool_shutdown_condition import WorkerPoolShutdownCondition


@dataclass
class NoRegisteredWorkersShutdownCondition(WorkerPoolShutdownCondition):
    """Specifies that a worker pool should be automatically shut down if no workers have been registered within the boot time limit."""
    type: str = field(default="co.yellowdog.platform.model.NoRegisteredWorkersShutdownCondition", init=False)
