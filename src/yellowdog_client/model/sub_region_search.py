from dataclasses import dataclass
from typing import List, Optional

from .cloud_provider import CloudProvider
from .sort_direction import SortDirection


@dataclass
class SubRegionSearch:
    providers: Optional[List[CloudProvider]] = None
    region: Optional[str] = None
    name: Optional[str] = None
    sortField: Optional[str] = None
    sortDirection: Optional[SortDirection] = None
