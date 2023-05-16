from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Optional

from .instance_status import InstanceStatus


@dataclass
class InstanceSummary:
    """Provides summary counts for instances provisioned from a compute source."""
    aliveCount: Optional[int] = field(default=None, init=False)
    statusCounts: Optional[Dict[InstanceStatus, int]] = None
    """A count of each status based on the non-expired instances that have been provisioned."""
    requestedCount: int = 0
    """The number of instances last requested from this compute source."""
    expectedCount: int = 0
    """The number of alive instances expected from this compute source, based on existing instances and the most recent provision action."""
    expiredCount: int = 0
    """The count of TERMINATED instances that have expired and can no longer be retrieved from the platform."""
    totalCount: int = 0
    """The total count of all instances provisioned from this compute source (including expired instances)."""
    lastUpdatedTime: Optional[datetime] = None
