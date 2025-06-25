from dataclasses import dataclass
from typing import Optional

from .sort_direction import SortDirection


@dataclass
class NamespaceSearch:
    namespace: Optional[str] = None
    deletable: Optional[bool] = None
    sortField: Optional[str] = None
    sortDirection: Optional[SortDirection] = None
