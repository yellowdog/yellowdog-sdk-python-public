from enum import Enum


class ImageOsType(Enum):
    LINUX = "LINUX"
    WINDOWS = "WINDOWS"

    def __str__(self) -> str:
        return self.name
