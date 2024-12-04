from enum import Enum


class GceHostMaintenanceBehaviour(Enum):
    """The GCE instance behaviour to apply on a host maintenance event."""
    MIGRATE = "MIGRATE"
    """Specifies that instances shall be live-migrated on a host maintenance event."""
    TERMINATE = "TERMINATE"
    """Specifies that instances shall be stopped on a host maintenance event."""

    def __str__(self) -> str:
        return self.name
