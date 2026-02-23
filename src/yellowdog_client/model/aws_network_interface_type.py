from __future__ import annotations

from enum import Enum


class AwsNetworkInterfaceType(Enum):
    code: str

    EFA_WITH_ENA = "EFA_WITH_ENA", "efa"
    EFA_ONLY = "EFA_ONLY", "efa-only"
    ENI = "ENI", "interface"

    def __new__(cls, value: str, code: str) -> AwsNetworkInterfaceType:
        obj = object.__new__(cls)
        obj._value_ = value
        obj.code = code
        return obj

    def __str__(self) -> str:
        return self.name
