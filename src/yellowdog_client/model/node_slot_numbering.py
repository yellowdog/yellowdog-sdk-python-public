from enum import Enum


class NodeSlotNumbering(Enum):
    REUSABLE = "REUSABLE"

    def __str__(self) -> str:
        return self.name
