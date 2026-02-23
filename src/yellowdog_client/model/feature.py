from __future__ import annotations

from enum import Enum


class Feature(Enum):
    title: str

    PLATFORM = "PLATFORM", "Platform"
    INDEX = "INDEX", "Index"
    INDEX_PRO = "INDEX_PRO", "Index Pro"

    def __new__(cls, value: str, title: str) -> Feature:
        obj = object.__new__(cls)
        obj._value_ = value
        obj.title = title
        return obj

    def __str__(self) -> str:
        return self.name
