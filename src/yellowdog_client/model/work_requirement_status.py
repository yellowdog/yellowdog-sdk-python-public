from enum import Enum


class WorkRequirementStatus(Enum):
    """
    Describes the status of a work requirement.

    The status of a work requirement provides an aggregated view of the statuses of the task groups within that requirement.
    """

    RUNNING = "RUNNING", False
    """The work requirement is in progress and its tasks can be executed."""
    HELD = "HELD", False
    """
    The work requirement has been held by the user and no further tasks will be executed until it is resumed.
    Task group resources (e.g. Workers) will be released.
    """

    COMPLETED = "COMPLETED", True
    """All task groups in the work requirement have been completed."""
    FAILED = "FAILED", True
    """All task groups in the work requirement have been finished but at least one has failed."""
    CANCELLING = "CANCELLING", False
    """The work requirement is in the process of cancelling, once no task groups are currently executing the status will become CANCELLED."""
    CANCELLED = "CANCELLED", True
    """The work requirement has been explicitly cancelled by the user."""

    def __new__(cls, value, finished: bool):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.finished = finished
        return obj

    def __str__(self) -> str:
        return self.name
