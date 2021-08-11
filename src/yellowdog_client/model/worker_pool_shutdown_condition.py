from dataclasses import dataclass, field


@dataclass
class WorkerPoolShutdownCondition:
    """Interface implemented by provisioned worker pool automatic shutdown conditions."""
    type: str = field(default=None, init=False)
