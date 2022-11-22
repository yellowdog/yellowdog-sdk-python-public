from enum import Enum


class WorkRequirementStatus(Enum):
    """
    Describes the status of a work requirement.

    The status of a work requirement provides an aggregated view of the statuses of the task groups within that requirement.
    """

    NEW = "NEW", False, False
    """The work requirement has been created and submitted to YellowDog Scheduler."""
    PENDING = "PENDING", False, False
    """The work requirement is waiting to be started once sufficient workers have been claimed."""
    UNFULFILLED = "UNFULFILLED", False, True
    """The work requirement was unable to claim sufficient workers on submit and has been finished."""
    RUNNING = "RUNNING", True, False
    """The work requirement is in progress and its tasks can be executed."""
    STARVED = "STARVED", True, False
    """The work requirement was in progress but it has lost all its workers and none of its tasks are being executed."""
    HELD = "HELD", False, False
    """The work requirement has been held by the user and no further tasks will be executed until it is resumed."""
    COMPLETED = "COMPLETED", False, True
    """All task groups in the work requirement have been successfully completed."""
    FAILED = "FAILED", False, True
    """All task groups in the work requirement have been finished and most may be completed but at least one has failed."""
    CANCELLING = "CANCELLING", False, False
    """The work requirement is in the process of cancelling, once no task groups are currently executing the status will become CANCELLED."""
    CANCELLED = "CANCELLED", False, True
    """The work requirement has been explicitly cancelled by the user."""

    def __new__(cls, value, active: bool, finished: bool):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.active = active
        obj.finished = finished
        return obj

    def __str__(self) -> str:
        return self.name
