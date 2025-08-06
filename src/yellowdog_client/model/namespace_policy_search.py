from dataclasses import dataclass
from typing import List, Optional

from .sort_direction import SortDirection


@dataclass
class NamespacePolicySearch:
    sortField: Optional[str] = None
    sortDirection: Optional[SortDirection] = None
    namespace: Optional[str] = None
    namespaces: Optional[List[str]] = None
