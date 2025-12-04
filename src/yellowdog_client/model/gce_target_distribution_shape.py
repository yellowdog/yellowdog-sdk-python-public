from enum import Enum


class GceTargetDistributionShape(Enum):
    EVEN = "EVEN"
    BALANCED = "BALANCED"
    ANY = "ANY"
    ANY_SINGLE_ZONE = "ANY_SINGLE_ZONE"

    def __str__(self) -> str:
        return self.name
