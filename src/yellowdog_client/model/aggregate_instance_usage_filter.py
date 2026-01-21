from dataclasses import dataclass
from datetime import datetime
from typing import List

from .filter import Filter
from .instance_status import InstanceStatus


@dataclass
class AggregateInstanceUsageFilter(Filter):
    fromTime: datetime
    untilTime: datetime
    instanceStatuses: List[InstanceStatus]
