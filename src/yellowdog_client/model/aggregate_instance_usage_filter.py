from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Set

from .filter import Filter
from .instance_status import InstanceStatus


@dataclass
class AggregateInstanceUsageFilter(Filter):
    fromTime: datetime
    untilTime: datetime
    instanceStatuses: Optional[List[InstanceStatus]] = None
    accountIds: Optional[Set[str]] = None
