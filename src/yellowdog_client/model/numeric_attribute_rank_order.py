from enum import Enum


class NumericAttributeRankOrder(Enum):
    PREFER_LOWER = "PREFER_LOWER"
    PREFER_HIGHER = "PREFER_HIGHER"

    def __str__(self) -> str:
        return self.name
