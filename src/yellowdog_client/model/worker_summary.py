from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Optional

from .worker_status import WorkerStatus


@dataclass
class WorkerSummary:
    """A summary of a group of workers."""
    statusCounts: Optional[Dict[WorkerStatus, int]] = None
    """The number of workers in each status."""
    allWorkerClaimsCount: int = 0
    """The number of claims across all workers in this worker pool."""
    claimedWorkerCount: int = 0
    """The number of workers that are claimed."""
    lastClaimedTime: Optional[datetime] = None
    """The last time one of these workers was claimed."""
    lastReleasedTime: Optional[datetime] = None
    """The last time one of these workers was released."""
    lastUpdatedTime: Optional[datetime] = None
    """The last time this summary was updated."""
