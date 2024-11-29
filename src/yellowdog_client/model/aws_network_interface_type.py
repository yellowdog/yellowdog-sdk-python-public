from enum import Enum


class AwsNetworkInterfaceType(Enum):
    EFA_WITH_ENA = "EFA_WITH_ENA", "efa"
    EFA_ONLY = "EFA_ONLY", "efa-only"
    ENI = "ENI", "interface"

    def __new__(cls, value, code: str):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.code = code
        return obj

    def __str__(self) -> str:
        return self.name
