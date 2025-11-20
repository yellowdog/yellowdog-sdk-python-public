from dataclasses import dataclass
from typing import Dict, List, Optional

from .sort_direction import SortDirection


@dataclass
class TrackSearch:
    namespaces: Optional[List[str]] = None
    tags: Optional[Dict[str, str]] = None
    sortField: Optional[str] = None
    sortDirection: Optional[SortDirection] = None
