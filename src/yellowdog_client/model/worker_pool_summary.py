from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from .identified import Identified
from .named import Named
from .worker_pool_status import WorkerPoolStatus


@dataclass
class WorkerPoolSummary(Identified, Named):
    """Provides a summary of a WorkerPool including the ID that can be used to retrieve the full object."""
    id: Optional[str] = None
    name: Optional[str] = None
    """The name used to uniquely identify the worker pool."""
    type: Optional[str] = None
    """The type of the worker pool."""
    registeredNodeCount: int = 0
    """The count of nodes that have registered with the worker pool."""
    registeredWorkerCount: int = 0
    """The count of workers that have registered with the worker pool."""
    claimedWorkerCount: int = 0
    """The count of workers within the worker pool that have been claimed by one or more task groups."""
    workingWorkerCount: int = 0
    """The count of workers within the worker pool that are currently doing a task."""
    status: Optional[WorkerPoolStatus] = None
    """The status of the worker pool."""
    createdTime: Optional[datetime] = None
    """The date and time when the worker pool was first created."""
    healthy: bool = False
    """Indicates if the worker pool is healthy. If false then workers may be late or lost."""
