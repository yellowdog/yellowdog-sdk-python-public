from __future__ import annotations

from enum import Enum


class InstancePricing(Enum):
    display_name: str

    ON_DEMAND_ONLY = "ON_DEMAND_ONLY", "On Demand only"
    SPOT_ONLY = "SPOT_ONLY", "Spot only"
    SPOT_AND_ON_DEMAND = "SPOT_AND_ON_DEMAND", "Spot and On Demand"

    def __new__(cls, value: str, display_name: str) -> InstancePricing:
        obj = object.__new__(cls)
        obj._value_ = value
        obj.display_name = display_name
        return obj

    def __str__(self) -> str:
        return self.name
