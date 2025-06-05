from enum import Enum


class WorkerStatus(Enum):
    """Describes the current status of a Worker."""
    DOING_TASK = "DOING_TASK", True, True
    """The Worker has been instructed to execute a task."""
    SLEEPING = "SLEEPING", True, True
    """The Worker has been instructed to sleep for a specified period of time."""
    STOPPED = "STOPPED", True, True
    """The Worker has been instructed to stop."""
    STARTING = "STARTING", True, True
    """The Agent has been instructed to start the Worker."""
    LATE = "LATE", True, False
    """The Worker's heartbeat is late."""
    LOST = "LOST", False, False
    """The Worker's heartbeat has not been received for long enough that the Worker is considered to have been lost."""
    FOUND = "FOUND", True, True
    """
    The Worker was considered to be lost but its heartbeat has returned, however it has not yet requested instruction.
    @deprecated Workers can no longer be FOUND once LOST. Status can be removed when all clients >= v9.3.0
    """

    SHUTDOWN = "SHUTDOWN", False, False
    """The Worker has been instructed to shut down."""

    def __new__(cls, value, available: bool, healthy: bool):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.available = available
        obj.healthy = healthy
        return obj

    def __str__(self) -> str:
        return self.name
