from dataclasses import dataclass
from typing import List, Optional

from .compute_requirement_status import ComputeRequirementStatus
from .sort_direction import SortDirection


@dataclass
class ComputeRequirementSearch:
    sortField: Optional[str] = None
    sortDirection: Optional[SortDirection] = None
    namespace: Optional[str] = None
    tag: Optional[str] = None
    statuses: Optional[List[ComputeRequirementStatus]] = None
