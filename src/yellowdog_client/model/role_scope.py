from dataclasses import dataclass
from typing import Optional, Set


@dataclass
class RoleScope:
    global_: bool = False
    namespaces: Optional[Set[str]] = None
