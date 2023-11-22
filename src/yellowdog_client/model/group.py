from dataclasses import dataclass, field
from typing import List, Optional

from .group_role import GroupRole
from .identified import Identified


@dataclass
class Group(Identified):
    id: Optional[str] = field(default=None, init=False)
    name: str
    description: Optional[str] = None
    roles: Optional[List[GroupRole]] = None
    adminGroup: bool = False
