from enum import Enum


class PermissionScope(Enum):
    GLOBAL_ONLY = "GLOBAL_ONLY"
    NAMESPACED_OR_GLOBAL = "NAMESPACED_OR_GLOBAL"

    def __str__(self) -> str:
        return self.name
