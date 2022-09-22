from enum import Enum


class OperatingSystemLicence(Enum):
    WINDOWS = "WINDOWS", "Windows"
    NONE = "NONE", "None"

    def __new__(cls, value, display_name: str):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.display_name = display_name
        return obj

    def __str__(self) -> str:
        return self.name
