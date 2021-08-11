from enum import Enum


class SortDirection(Enum):
    ASCENDING = "ASCENDING"
    DESCENDING = "DESCENDING"

    def __str__(self) -> str:
        return self.name
