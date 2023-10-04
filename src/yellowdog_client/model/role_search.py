from dataclasses import dataclass
from typing import Optional

from .permission import Permission
from .sort_direction import SortDirection


@dataclass
class RoleSearch:
    sortField: Optional[str] = None
    sortDirection: Optional[SortDirection] = None
    name: Optional[str] = None
    permission: Optional[Permission] = None
