from dataclasses import dataclass
from typing import List, Optional

from .instant_range import InstantRange
from .sort_direction import SortDirection
from .work_requirement_status import WorkRequirementStatus


@dataclass
class WorkRequirementSearch:
    namespace: Optional[str] = None
    name: Optional[str] = None
    tag: Optional[str] = None
    statuses: Optional[List[WorkRequirementStatus]] = None
    isHealthy: Optional[bool] = None
    createdTime: Optional[InstantRange] = None
    sortField: Optional[str] = None
    sortDirection: Optional[SortDirection] = None
