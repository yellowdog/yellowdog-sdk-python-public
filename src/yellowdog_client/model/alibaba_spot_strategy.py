from enum import Enum


class AlibabaSpotStrategy(Enum):
    NO_SPOT = "NO_SPOT", "NoSpot"
    SPOT_WITH_PRICE_LIMIT = "SPOT_WITH_PRICE_LIMIT", "SpotWithPriceLimit"
    SPOT_AS_PRICE_GO = "SPOT_AS_PRICE_GO", "SpotAsPriceGo"

    def __new__(cls, value, code: str):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.code = code
        return obj

    def __str__(self) -> str:
        return self.name
