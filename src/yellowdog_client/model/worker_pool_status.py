from enum import Enum


class WorkerPoolStatus(Enum):
    """Indicates the status of a worker pool"""
    PENDING = "PENDING"
    """The worker pool has been started but no workers have yet registered"""
    CONFIGURING = "CONFIGURING"
    """The nodes in the worker pool are being identified and their node types are being set"""
    EMPTY = "EMPTY"
    """The worker pool has no registered workers"""
    IDLE = "IDLE"
    """The worker pool has registered workers but none are currently claimed"""
    RUNNING = "RUNNING"
    """One or more workers are claimed"""
    SHUTDOWN = "SHUTDOWN"
    """The worker pool is shutdown and any workers are instructed to shutdown"""

    def is_available(self) -> bool:
        return self in (self.PENDING, self.EMPTY, self.IDLE, self.RUNNING)

    def __str__(self) -> str:
        return self.name
