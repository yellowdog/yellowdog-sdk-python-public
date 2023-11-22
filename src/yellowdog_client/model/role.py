from dataclasses import dataclass, field
from typing import Optional, Set

from .identified import Identified
from .permission import Permission


@dataclass
class Role(Identified):
    id: Optional[str] = field(default=None, init=False)
    name: str
    permissions: Set[Permission]
    description: Optional[str] = None
