from enum import Enum


class NodeIdFilter(Enum):
    LIST = "LIST"
    EVENT = "EVENT"

    def __str__(self) -> str:
        return self.name
