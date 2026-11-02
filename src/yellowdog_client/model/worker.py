from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from .identified import Identified
from .worker_status import WorkerStatus


@dataclass
class Worker(Identified):
    """Describes a Worker managed by the YellowDog Scheduler service."""
    id: Optional[str] = None
    status: Optional[WorkerStatus] = None
    """The status of the worker."""
    taskGroupId: Optional[str] = None
    """The ID of the task group that has a claim on the worker, if any. A worker is claimed by at most one task group."""
    registeredTime: Optional[datetime] = None
    """The time at which the worker was registered."""
