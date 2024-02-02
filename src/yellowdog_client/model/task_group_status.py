from enum import Enum


class TaskGroupStatus(Enum):
    """
    Describes the status of a task group.

    The status of the task group provides an aggregated view of the statuses of tasks within the task group.
    """

    PENDING = "PENDING", False, False
    """The task group is awaiting resources required to execute tasks."""
    RUNNING = "RUNNING", False, False
    """The task group has sufficient resources to execute tasks."""
    HELD = "HELD", False, False
    """
    The task group parent work requirement has been held by the user such that no further tasks are executed.
    Resources (e.g. Workers) will be released.
    The task group will remain in HELD state until the user reactivates the parent work requirement.
    """

    COMPLETED = "COMPLETED", False, True
    """All tasks within the task group have been completed."""
    FAILING = "FAILING", True, False
    """At least one task in the task group has failed and the task group is in the process of discarding any outstanding tasks."""
    FAILED = "FAILED", False, True
    """All tasks within the task group have been finished but at least one has failed."""
    CANCELLING = "CANCELLING", True, False
    """The parent work requirement is in the process of being cancelled, no further tasks will be executed."""
    CANCELLED = "CANCELLED", False, True
    """The parent work requirement has been cancelled, no tasks are currently being executed or will be executed."""

    def __new__(cls, value, finishing: bool, finished: bool):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.finishing = finishing
        obj.finished = finished
        return obj

    def __str__(self) -> str:
        return self.name
