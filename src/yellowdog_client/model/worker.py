from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from .identified import Identified
from .worker_status import WorkerStatus


@dataclass
class Worker(Identified):
    """Describes a Worker managed by the YellowDog Scheduler service."""
    id: Optional[str] = None
    status: Optional[WorkerStatus] = None
    """The status of the worker."""
    taskGroupIds: Optional[List[str]] = None
    """The IDs of the task groups which have claims on the worker."""
    claimCount: int = 0
    """A count of the tasks groups which have claims on the worker. Always identical to the size of #taskGroupIds."""
    exclusive: bool = False
    """Indicates if the worker is exclusively claimed by a single task group."""
    currentTaskId: Optional[str] = None
    """The ID of the task currently allocated to the worker."""
    registeredTime: Optional[datetime] = None
    """The time at which the worker was registered."""
