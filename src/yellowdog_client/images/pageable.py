from dataclasses import dataclass, field
from typing import Optional

from .sort import Sort


@dataclass
class Pageable:
    unpaged: bool = field(default=None, init=False)
    paged: bool = False
    pageNumber: int = 0
    pageSize: int = 0
    offset: int = 0
    sort: Optional[Sort] = None
