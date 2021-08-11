from enum import Enum


class WorkRequirementStatus(Enum):
    """
    Describes the status of a work requirement.

    The status of a work requirement provides an aggregated view of the statuses of the task groups within that requirement.
    """

    NEW = "NEW"
    """The work requirement has been created and submitted to YellowDog Scheduler."""
    PENDING = "PENDING"
    """The work requirement is waiting to be started once sufficient workers have been claimed."""
    UNFULFILLED = "UNFULFILLED"
    """The work requirement was unable to claim sufficient workers on submit and has been finished."""
    WORKING = "WORKING"
    """The work requirement is in progress and its tasks are being executed."""
    STARVED = "STARVED"
    """The work requirement was in progress but it has lost all its workers and none of its tasks are being executed."""
    HELD = "HELD"
    """The work requirement has been held by the user and no further tasks will be executed until it is resumed."""
    COMPLETED = "COMPLETED"
    """All task groups in the work requirement have been successfully completed."""
    FAILED = "FAILED"
    """All task groups in the work requirement have been finished and most may be completed but at least one has failed."""
    CANCELLING = "CANCELLING"
    """The work requirement is in the process of cancelling, once no task groups are currently executing the status will become CANCELLED."""
    CANCELLED = "CANCELLED"
    """The work requirement has been explicitly cancelled by the user."""

    def is_active(self) -> bool:
        return self in (self.WORKING, self.STARVED)

    def is_finished(self) -> bool:
        return self in (self.UNFULFILLED, self.COMPLETED, self.FAILED, self.CANCELLED)

    def __str__(self) -> str:
        return self.name
