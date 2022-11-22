from enum import Enum


class TaskInputVerification(Enum):
    """Indicates if the Scheduler should verify the existence of a task input prior to starting the task."""
    VERIFY_AT_START = "VERIFY_AT_START"
    """The task input must exist at the time when the task group is started, otherwise the task is FAILED."""
    VERIFY_WAIT = "VERIFY_WAIT"
    """The task will remain in PENDING until the task input exists."""

    def __str__(self) -> str:
        return self.name
