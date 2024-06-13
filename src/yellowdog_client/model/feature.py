from enum import Enum


class Feature(Enum):
    PLATFORM = "PLATFORM", "Platform"
    INDEX = "INDEX", "Index"
    INDEX_PRO = "INDEX_PRO", "Index Pro"

    def __new__(cls, value, title: str):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.title = title
        return obj

    def __str__(self) -> str:
        return self.name
