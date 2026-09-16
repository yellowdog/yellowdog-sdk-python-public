from dataclasses import dataclass
from typing import Optional

from .sort_direction import SortDirection


@dataclass
class KeyringSearch:
    sortField: Optional[str] = None
    sortDirection: Optional[SortDirection] = None
    name: Optional[str] = None
