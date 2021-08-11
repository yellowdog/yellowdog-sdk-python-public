from enum import Enum


class WorkerStatus(Enum):
    """Describes the current status of a Worker."""
    DOING_TASK = "DOING_TASK"
    """The Worker has been instructed to execute a task."""
    SLEEPING = "SLEEPING"
    """The Worker has been instructed to sleep for a specified period of time."""
    LATE = "LATE"
    """The Worker's heartbeat is late."""
    LOST = "LOST"
    """The Worker's heartbeat has not been received for long enough that the Worker is considered to have been lost."""
    FOUND = "FOUND"
    """The Worker was considered to be lost but its heartbeat has returned, however it has not yet requested instruction."""
    SHUTDOWN = "SHUTDOWN"
    """The Worker has been instructed to shutdown"""

    def is_active(self) -> bool:
        return self in (self.DOING_TASK, self.SLEEPING, self.LATE, self.FOUND)

    def is_healthy(self) -> bool:
        return self in (self.DOING_TASK, self.SLEEPING, self.FOUND)

    def __str__(self) -> str:
        return self.name
