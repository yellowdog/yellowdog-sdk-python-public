from dataclasses import dataclass
from typing import List, Optional

from .sort_direction import SortDirection


@dataclass
class ComputeRequirementTemplateSearch:
    sortField: Optional[str] = None
    sortDirection: Optional[SortDirection] = None
    name: Optional[str] = None
    namespaces: Optional[List[str]] = None
    type: Optional[List[str]] = None
    strategyType: Optional[List[str]] = None
