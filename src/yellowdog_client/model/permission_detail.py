from dataclasses import dataclass
from typing import Optional, Set

from .permission_scope import PermissionScope


@dataclass
class PermissionDetail:
    name: Optional[str] = None
    title: Optional[str] = None
    includes: Optional[Set[str]] = None
    scope: Optional[PermissionScope] = None
