from enum import Enum


class WorkerPoolStatus(Enum):
    """Indicates the status of a worker pool"""
    PENDING = "PENDING", True, False
    """The worker pool has been started but no workers have yet registered."""
    CONFIGURING = "CONFIGURING", False, False
    """The nodes in the worker pool are being identified and their node types are being set."""
    EMPTY = "EMPTY", True, False
    """The worker pool has no registered workers."""
    IDLE = "IDLE", True, False
    """The worker pool has registered workers but none are currently claimed."""
    RUNNING = "RUNNING", True, False
    """One or more workers are claimed."""
    SHUTDOWN = "SHUTDOWN", False, True
    """The worker pool is shutdown and any workers are instructed to shutdown."""
    TERMINATED = "TERMINATED", False, True
    """The worker pool is terminated and the associated compute requirement is terminated (provisioned worker pool) or all nodes have shutdown (configured worker pool)."""

    def __new__(cls, value, available: bool, finished: bool):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.available = available
        obj.finished = finished
        return obj

    def __str__(self) -> str:
        return self.name
