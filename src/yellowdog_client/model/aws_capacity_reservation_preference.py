from enum import Enum


class AwsCapacityReservationPreference(Enum):
    NONE = "NONE"
    OPEN = "OPEN"
    CAPACITY_RESERVATIONS_ONLY = "CAPACITY_RESERVATIONS_ONLY"

    def __str__(self) -> str:
        return self.name
