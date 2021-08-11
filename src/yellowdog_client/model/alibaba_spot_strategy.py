from enum import Enum


class AlibabaSpotStrategy(Enum):
    NO_SPOT = "NO_SPOT"
    SPOT_WITH_PRICE_LIMIT = "SPOT_WITH_PRICE_LIMIT"
    SPOT_AS_PRICE_GO = "SPOT_AS_PRICE_GO"

    def __str__(self) -> str:
        return self.name
