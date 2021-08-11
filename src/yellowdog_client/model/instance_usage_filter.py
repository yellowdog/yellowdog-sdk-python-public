from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from .filter import Filter


@dataclass
class InstanceUsageFilter(Filter):
    fromTime: datetime
    untilTime: datetime
    createdById: Optional[str] = None
    namespaces: Optional[List[str]] = None
    requirements: Optional[List[str]] = None
