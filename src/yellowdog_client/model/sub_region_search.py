from dataclasses import dataclass
from typing import List, Optional

from .cloud_provider import CloudProvider
from .slice_reference import SliceReference
from .sort_direction import SortDirection


@dataclass
class SubRegionSearch:
    providers: Optional[List[CloudProvider]] = None
    region: Optional[str] = None
    name: Optional[str] = None
    sliceReference: Optional[SliceReference] = None
    sortField: Optional[str] = None
    sortDirection: Optional[SortDirection] = None
