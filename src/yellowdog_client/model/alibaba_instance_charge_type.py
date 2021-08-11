from enum import Enum


class AlibabaInstanceChargeType(Enum):
    PRE_PAID = "PRE_PAID"
    POST_PAID = "POST_PAID"

    def __str__(self) -> str:
        return self.name
