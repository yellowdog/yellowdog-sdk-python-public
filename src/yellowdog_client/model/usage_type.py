from enum import Enum


class UsageType(Enum):
    ON_DEMAND = "ON_DEMAND"
    SPOT = "SPOT"

    def __str__(self) -> str:
        return self.name
