from enum import Enum


class AllowanceLimitEnforcement(Enum):
    """Defines the limit enforcement options for an empty allowance"""
    SOFT = "SOFT"
    """Existing operations will not be terminated but new operations will be disallowed"""
    HARD = "HARD"
    """Existing operations will be terminated, possibly after a grace period, and new operations will be disallowed"""

    def __str__(self) -> str:
        return self.name
