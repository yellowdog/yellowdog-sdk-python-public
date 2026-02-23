from __future__ import annotations

from enum import Enum


class AttributeSourceType(Enum):
    prefix: str

    SOURCE = "SOURCE", "source."
    USER = "USER", "user."
    EXTERNAL = "EXTERNAL", None

    def __new__(cls, value: str, prefix: str) -> AttributeSourceType:
        obj = object.__new__(cls)
        obj._value_ = value
        obj.prefix = prefix
        return obj

    def __str__(self) -> str:
        return self.name
