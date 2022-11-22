from enum import Enum


class TaskGroupStatus(Enum):
    """
    Describes the status of a task group.

    The status of the task group provides an aggregated view of the statuses of tasks within the task group.
    """

    NEW = "NEW", False, False, False, False
    """The task group has been created and submitted to YellowDog Scheduler."""
    PENDING = "PENDING", False, False, False, False
    """
    The task group has been submitted and YellowDog Scheduler is in the process of claiming workers to start the task group.
    The task group will remain in PENDING state until the minimum required number of workers has been claimed.
    """

    READY = "READY", False, False, False, False
    """
    The task group has claimed at least the minimum required number of workers and is ready to start running.
    The task group will remain in READY state until the WorkRequirement is started.
    """

    UNFULFILLED = "UNFULFILLED", False, False, False, True
    """The task group (or parent work requirement) was unable to claim the minimum required number of workers to start running and fulfilOnSubmit was specified for the work requirement."""
    WAITING = "WAITING", True, False, False, False
    """The task group has been started but is waiting for a dependency task group to complete before executing any tasks."""
    RUNNING = "RUNNING", True, True, False, False
    """The task group is running and tasks can be executed by Workers."""
    STARVED = "STARVED", True, True, False, False
    """The task group was in progress but it has lost all its workers and none of its tasks are being executed."""
    HELD = "HELD", True, False, False, False
    """
    The task group has been started and may have been running but the parent work requirement has been held by the user such that no further tasks are executed.
    The task group will remain in HELD state until the user reactivates the parent work requirement.
    """

    COMPLETED = "COMPLETED", True, False, False, True
    """All tasks within the task group have been completed."""
    FAILING = "FAILING", True, False, True, False
    """At least one task in the task group has failed and the task group is in the process of discarding any outstanding tasks."""
    FAILED = "FAILED", True, False, False, True
    """All tasks within the task group have been finished and most may be completed but at least one has failed."""
    CANCELLING = "CANCELLING", True, False, True, False
    """The parent work requirement is in the process of being cancelled, no further tasks will be executed."""
    CANCELLED = "CANCELLED", True, False, False, True
    """The parent work requirement has been cancelled, no tasks are currently being executed or will be executed."""

    def __new__(cls, value, started: bool, active: bool, finishing: bool, finished: bool):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.started = started
        obj.active = active
        obj.finishing = finishing
        obj.finished = finished
        return obj

    def __str__(self) -> str:
        return self.name
