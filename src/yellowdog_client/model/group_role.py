from dataclasses import dataclass

from .granted_permission_scope import GrantedPermissionScope
from .role_summary import RoleSummary


@dataclass
class GroupRole:
    role: RoleSummary
    scope: GrantedPermissionScope
