from enum import Enum


class TaskGroupStatus(Enum):
    """
    Describes the status of a task group.

    The status of the task group provides an aggregated view of the statuses of tasks within the task group.
    """

    NEW = "NEW"
    """The task group has been created and submitted to YellowDog Scheduler."""
    PENDING = "PENDING"
    """
    The task group has been submitted and YellowDog Scheduler is in the process of claiming workers to start the task group.
    The task group will remain in PENDING state until the minimum required number of workers has been claimed.
    """

    READY = "READY"
    """
    The task group has claimed at least the minimum required number of workers and is ready to start working.
    The task group will remain in READY state until the WorkRequirement is started.
    """

    UNFULFILLED = "UNFULFILLED"
    """The task group (or parent work requirement) was unable to claim the minimum required number of workers to start working and fulfilOnSubmit was specified for the work requirement."""
    WAITING = "WAITING"
    """The task group has been started but is waiting for a dependency task group to complete before executing any tasks."""
    WORKING = "WORKING"
    """The task group is running and tasks are being executed by Workers."""
    STARVED = "STARVED"
    """The task group was in progress but it has lost all its workers and none of its tasks are being executed."""
    HELD = "HELD"
    """
    The task group has been started and may have been running but the parent work requirement has been held by the user such that no further tasks are executed.
    The task group will remain in HELD state until the user reactivates the parent work requirement.
    """

    COMPLETED = "COMPLETED"
    """All tasks within the task group have been completed."""
    FAILING = "FAILING"
    """All tasks within the task group have been finished and most may be completed but at least one has failed."""
    FAILED = "FAILED"
    """All tasks within the task group have been finished and most may be completed but at least one has failed."""
    CANCELLING = "CANCELLING"
    """The parent work requirement is in the process of being cancelled, no further tasks will be executed."""
    CANCELLED = "CANCELLED"
    """The parent work requirement has been cancelled, no tasks are currently being executed or will be executed."""

    def is_active(self) -> bool:
        return self in (self.WORKING, self.STARVED)

    def is_finished(self) -> bool:
        return self in (self.UNFULFILLED, self.COMPLETED, self.FAILED, self.CANCELLED)

    def is_finishing(self) -> bool:
        return self in (self.FAILING, self.CANCELLING)

    def is_started(self) -> bool:
        return self in (self.WAITING, self.WORKING, self.STARVED, self.HELD, self.COMPLETED, self.FAILING, self.FAILED, self.CANCELLING, self.CANCELLED)

    def __str__(self) -> str:
        return self.name
