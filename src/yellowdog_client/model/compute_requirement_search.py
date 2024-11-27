from dataclasses import dataclass
from typing import List, Optional

from .compute_requirement_status import ComputeRequirementStatus
from .instant_range import InstantRange
from .sort_direction import SortDirection


@dataclass
class ComputeRequirementSearch:
    name: Optional[str] = None
    namespace: Optional[str] = None
    tag: Optional[str] = None
    statuses: Optional[List[ComputeRequirementStatus]] = None
    createdTime: Optional[InstantRange] = None
    sortField: Optional[str] = None
    sortDirection: Optional[SortDirection] = None
