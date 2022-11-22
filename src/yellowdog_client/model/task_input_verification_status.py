from enum import Enum


class TaskInputVerificationStatus(Enum):
    """Describes the status of a task input that requires verification."""
    WAITING = "WAITING"
    """The Scheduler is waiting for notification that the task input exists."""
    VERIFIED = "VERIFIED"
    """The task input has been verified and exists."""
    FAILED = "FAILED"
    """The task input does not exist."""

    def __str__(self) -> str:
        return self.name
