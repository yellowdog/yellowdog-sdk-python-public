from dataclasses import dataclass
from typing import List, Optional

from .cluster_status import ClusterStatus
from .instant_range import InstantRange
from .sort_direction import SortDirection


@dataclass
class ClusterSearch:
    name: Optional[str] = None
    namespaces: Optional[List[str]] = None
    statuses: Optional[List[ClusterStatus]] = None
    createdTime: Optional[InstantRange] = None
    sortField: Optional[str] = None
    sortDirection: Optional[SortDirection] = None
