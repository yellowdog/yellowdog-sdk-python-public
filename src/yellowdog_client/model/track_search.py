from dataclasses import dataclass
from typing import Dict, Optional

from .sort_direction import SortDirection


@dataclass
class TrackSearch:
    tags: Optional[Dict[str, str]] = None
    sortField: Optional[str] = None
    sortDirection: Optional[SortDirection] = None
