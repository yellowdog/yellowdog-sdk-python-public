from enum import Enum


class TaskStatus(Enum):
    """Describes the status of task."""
    PENDING = "PENDING", False, False
    """The task is waiting to be allocated and executed."""
    ALLOCATED = "ALLOCATED", True, False
    """The task has been allocated to a worker to be executed."""
    DOWNLOADING = "DOWNLOADING", True, False
    """The task inputs are being downloaded by its allocated worker."""
    RUNNING = "RUNNING", True, False
    """The task is being executed by its allocated worker."""
    UPLOADING = "UPLOADING", True, False
    """The task outputs are being uploaded by its allocated worker."""
    COMPLETED = "COMPLETED", False, True
    """The task has been completed."""
    FAILED = "FAILED", False, True
    """The task has failed."""
    ABORTED = "ABORTED", False, True
    """The task has been aborted whilst in progress."""
    CANCELLED = "CANCELLED", False, True
    """The task has been cancelled by the user."""
    DISCARDED = "DISCARDED", False, True
    """The task will not be allocated as its task group has finished."""

    def __new__(cls, value, in_progress: bool, finished: bool):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.in_progress = in_progress
        obj.finished = finished
        return obj

    def __str__(self) -> str:
        return self.name
