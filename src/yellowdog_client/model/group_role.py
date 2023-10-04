from dataclasses import dataclass

from .role_summary import RoleSummary


@dataclass
class GroupRole:
    role: RoleSummary
