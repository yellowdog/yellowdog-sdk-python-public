from dataclasses import dataclass
from typing import List, Optional

from .instant_range import InstantRange
from .sort_direction import SortDirection
from .worker_pool_status import WorkerPoolStatus


@dataclass
class WorkerPoolSearch:
    namespace: Optional[str] = None
    name: Optional[str] = None
    type: Optional[str] = None
    statuses: Optional[List[WorkerPoolStatus]] = None
    createdTime: Optional[InstantRange] = None
    isHealthy: Optional[bool] = None
    sortField: Optional[str] = None
    sortDirection: Optional[SortDirection] = None
