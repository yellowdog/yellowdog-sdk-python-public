from dataclasses import dataclass
from typing import Dict, Optional

from .granted_permission_scope import GrantedPermissionScope
from .permission import Permission


@dataclass
class GrantedPermissions:
    permissions: Optional[Dict[Permission, GrantedPermissionScope]] = None
