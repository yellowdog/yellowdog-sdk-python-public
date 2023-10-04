from dataclasses import dataclass
from typing import Optional

from .sort_direction import SortDirection


@dataclass
class GroupSearch:
    sortField: Optional[str] = None
    sortDirection: Optional[SortDirection] = None
    name: Optional[str] = None
