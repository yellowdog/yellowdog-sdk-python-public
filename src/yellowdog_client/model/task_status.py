from __future__ import annotations

from enum import Enum


class TaskStatus(Enum):
    """Describes the status of task."""
    waiting: bool
    """Returns true, if the task status indicates that it is waiting either for resources, or to be allocated; otherwise, false."""
    in_progress: bool
    """Returns true, if the task status indicates that it is currently in progress; otherwise, false."""
    finished: bool
    """Returns true, if the task status indicates that the task is finished; otherwise, false."""

    PENDING = "PENDING", True, False, False
    """The task is waiting for resources to be verified."""
    READY = "READY", True, False, False
    """The task is ready to be allocated and executed."""
    ALLOCATED = "ALLOCATED", False, True, False
    """The task has been allocated to a worker to be executed."""
    DOWNLOADING = "DOWNLOADING", False, True, False
    """The task inputs are being downloaded by its allocated worker."""
    EXECUTING = "EXECUTING", False, True, False
    """The task is being executed by its allocated worker."""
    UPLOADING = "UPLOADING", False, True, False
    """The task outputs are being uploaded by its allocated worker."""
    COMPLETED = "COMPLETED", False, False, True
    """The task has been completed."""
    FAILED = "FAILED", False, False, True
    """The task has failed."""
    ABORTED = "ABORTED", False, False, True
    """The task has been aborted whilst in progress."""
    CANCELLED = "CANCELLED", False, False, True
    """The task has been cancelled by the user."""
    DISCARDED = "DISCARDED", False, False, True
    """The task will not be allocated as its task group has finished."""

    def __new__(cls, value: str, waiting: bool, in_progress: bool, finished: bool) -> TaskStatus:
        obj = object.__new__(cls)
        obj._value_ = value
        obj.waiting = waiting
        obj.in_progress = in_progress
        obj.finished = finished
        return obj

    def __str__(self) -> str:
        return self.name
