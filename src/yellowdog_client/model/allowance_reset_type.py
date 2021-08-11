from enum import Enum


class AllowanceResetType(Enum):
    """Defines when, or if, an allowance will reset the used amount back to zero"""
    NONE = "NONE"
    """The allowance does not reset"""
    DAYS = "DAYS"
    """The allowance resets after a configured number of days"""
    MONTHS = "MONTHS"
    """The allowance resets after a configured number of months"""

    def __str__(self) -> str:
        return self.name
