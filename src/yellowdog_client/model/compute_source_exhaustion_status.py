from enum import Enum


class ComputeSourceExhaustionStatus(Enum):
    LIMITED = "LIMITED"
    LIMITED_AWAITING_TERMINATION = "LIMITED_AWAITING_TERMINATION"
    TERMINATION = "TERMINATION"

    def __str__(self) -> str:
        return self.name
