from dataclasses import dataclass
from typing import List, Optional

from .sort_direction import SortDirection


@dataclass
class ComputeSourceTemplateSearch:
    sortField: Optional[str] = None
    name: Optional[str] = None
    sortDirection: Optional[SortDirection] = None
    namespaces: Optional[List[str]] = None
    sourceType: Optional[str] = None
    sourceTypes: Optional[List[str]] = None
