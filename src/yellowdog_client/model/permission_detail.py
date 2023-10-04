from dataclasses import dataclass
from typing import Optional, Set


@dataclass
class PermissionDetail:
    name: Optional[str] = None
    title: Optional[str] = None
    includes: Optional[Set[str]] = None
