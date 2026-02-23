from __future__ import annotations

from enum import Enum


class OperatingSystemLicence(Enum):
    display_name: str

    WINDOWS = "WINDOWS", "Windows"
    NONE = "NONE", "None"

    def __new__(cls, value: str, display_name: str) -> OperatingSystemLicence:
        obj = object.__new__(cls)
        obj._value_ = value
        obj.display_name = display_name
        return obj

    def __str__(self) -> str:
        return self.name
