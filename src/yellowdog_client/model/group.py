from dataclasses import dataclass, field
from typing import List, Optional

from .group_role import GroupRole


@dataclass
class Group:
    id: Optional[str] = field(default=None, init=False)
    name: str
    description: Optional[str] = None
    roles: Optional[List[GroupRole]] = None
    adminGroup: bool = False
