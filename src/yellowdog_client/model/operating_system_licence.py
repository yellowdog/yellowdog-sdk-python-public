from enum import Enum


class OperatingSystemLicence(Enum):
    WINDOWS = "WINDOWS"
    NONE = "NONE"

    def __str__(self) -> str:
        return self.name
