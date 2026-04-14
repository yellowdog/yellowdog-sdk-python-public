from __future__ import annotations

from enum import Enum


class WorkerStatus(Enum):
    """Describes the current status of a Worker."""
    available: bool
    """Returns true, if the status indicates the Worker is currently available; otherwise, false."""
    healthy: bool
    """Returns true, if the status indicates the Worker is currently healthy; otherwise, false."""

    DOING_TASK = "DOING_TASK", True, True
    """
    The Worker has been instructed to execute a task.

    .. deprecated:: (unknown)
        only used by single allocation
    """

    SLEEPING = "SLEEPING", True, True
    """
    The Worker is claimed by one or more task groups but has been instructed to sleep as no tasks are READY for it.

    .. deprecated:: (unknown)
        only used by single allocation
    """

    STOPPED = "STOPPED", True, True
    """The Worker is not claimed and has been instructed to stop."""
    STARTING = "STARTING", True, True
    """The Worker has become claimed and the Agent has been instructed to start the Worker."""
    BATCH_ALLOCATION = "BATCH_ALLOCATION", True, True
    """
    The Worker has become claimed for batch allocation. Its status is now monitored locally to the node.

    .. deprecated:: (unknown)
        the value :attr:`WorkerStatus.RUNNING` is now used instead.
    """

    LATE = "LATE", True, False
    """The Worker's heartbeat is late."""
    LOST = "LOST", False, False
    """The Worker's heartbeat has not been received for long enough that the Worker is considered to have been lost."""
    RUNNING = "RUNNING", True, True
    """The Worker has become claimed. Its status is now monitored locally to the node."""
    SHUTDOWN = "SHUTDOWN", False, False
    """The Worker has been instructed to shut down."""

    def __new__(cls, value: str, available: bool, healthy: bool) -> WorkerStatus:
        obj = object.__new__(cls)
        obj._value_ = value
        obj.available = available
        obj.healthy = healthy
        return obj

    def __str__(self) -> str:
        return self.name
