from enum import Enum


class AlibabaInstanceChargeType(Enum):
    PRE_PAID = "PRE_PAID", "PrePaid"
    POST_PAID = "POST_PAID", "PostPaid"

    def __new__(cls, value, code: str):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.code = code
        return obj

    def __str__(self) -> str:
        return self.name
