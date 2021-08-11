from enum import Enum


class AttributeSourceType(Enum):
    SOURCE = "SOURCE"
    USER = "USER"
    EXTERNAL = "EXTERNAL"

    def __str__(self) -> str:
        return self.name
