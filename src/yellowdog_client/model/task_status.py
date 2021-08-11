from enum import Enum


class TaskStatus(Enum):
    """Describes the status of task."""
    PENDING = "PENDING"
    """The task is waiting to be allocated and executed."""
    ALLOCATED = "ALLOCATED"
    """The task has been allocated to a worker to be executed."""
    DOWNLOADING = "DOWNLOADING"
    """The task inputs are being downloaded by its allocated worker."""
    RUNNING = "RUNNING"
    """The task is being executed by its allocated worker."""
    UPLOADING = "UPLOADING"
    """The task outputs are being uploaded by its allocated worker."""
    COMPLETED = "COMPLETED"
    """The task has been completed."""
    FAILED = "FAILED"
    """The task has failed."""
    CANCELLED = "CANCELLED"
    """The task has been cancelled by the user."""
    DISCARDED = "DISCARDED"
    """The task will not be allocated as its task group has finished."""

    def is_finished(self) -> bool:
        return self in (self.COMPLETED, self.FAILED, self.CANCELLED, self.DISCARDED)

    def is_in_progress(self) -> bool:
        return self in (self.ALLOCATED, self.DOWNLOADING, self.RUNNING, self.UPLOADING)

    def __str__(self) -> str:
        return self.name
