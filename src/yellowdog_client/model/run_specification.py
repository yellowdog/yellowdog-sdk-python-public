from dataclasses import dataclass
from typing import List, Optional

from .cloud_provider import CloudProvider
from .double_range import DoubleRange
from .worker_claim_behaviour import WorkerClaimBehaviour
from .worker_release_behaviour import WorkerReleaseBehaviour


@dataclass
class RunSpecification:
    """Specifies the behaviours to be used by the YellowDog Scheduler when executing Tasks within the associated TaskGroup."""
    taskTypes: List[str]
    """The task types that will be used in the associated TaskGroup."""
    instanceTypes: Optional[List[str]] = None
    """The machine instance types that can be used to execute tasks"""
    vcpus: Optional[DoubleRange] = None
    """Range constraint on number of vCPUs that are required to execute tasks"""
    ram: Optional[DoubleRange] = None
    """Range constraint on GB of RAM that are required to execute tasks"""
    minimumQueueConcurrency: int = 0
    """The minimum number of Workers that must be claimed before starting the associated TaskGroup."""
    idealQueueConcurrency: int = 0
    """The ideal number of Workers that should be claimed for the associated TaskGroup."""
    workerClaimBehaviour: WorkerClaimBehaviour = WorkerClaimBehaviour.STARTUP_ONLY
    workerReleaseBehaviour: WorkerReleaseBehaviour = WorkerReleaseBehaviour.NO_PENDING_TASKS
    """Defines the behaviour the YellowDog Scheduler should use when releasing Workers from the associated TaskGroup."""
    shareWorkers: Optional[bool] = False
    """If true, then allow claimed Workers to be shared with other task groups; otherwise, Workers are exclusive."""
    maximumTaskRetries: int = 0
    """The maximum number of times a task can be retried after it has failed."""
    providers: Optional[List[CloudProvider]] = None
    """Constrains the YellowDog Scheduler to only execute tasks from the associated TaskGroup on the specified providers."""
    regions: Optional[List[str]] = None
    """Constrains the YellowDog Scheduler to only execute tasks from the associated TaskGroup in the specified regions."""
    workerTags: Optional[List[str]] = None
    """Constrains the YellowDog Scheduler to only execute tasks from the associated TaskGroup on workers with a matching tag value."""
