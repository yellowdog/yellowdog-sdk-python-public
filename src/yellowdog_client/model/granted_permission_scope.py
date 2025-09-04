from dataclasses import dataclass
from typing import List, Optional

from .namespace_ref import NamespaceRef


@dataclass
class GrantedPermissionScope:
    global_: bool = False
    namespaces: Optional[List[NamespaceRef]] = None
