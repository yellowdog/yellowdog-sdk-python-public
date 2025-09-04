from dataclasses import dataclass, field
from typing import List, Optional

from .identified import Identified
from .permission import Permission


@dataclass
class Role(Identified):
    id: Optional[str] = field(default=None, init=False)
    name: str
    permissions: List[Permission]
    description: Optional[str] = None
