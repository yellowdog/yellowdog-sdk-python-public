from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from .task_error_type import TaskErrorType
from .task_status import TaskStatus


@dataclass
class TaskError:
    """Holds details of an error that occurred during execution of the task."""
    timestamp: datetime
    """The time at which the error occurred."""
    error: str
    """A description of the error."""
    workerId: Optional[str] = None
    """The ID of the worker where the error occurred."""
    errorType: str = TaskErrorType.UNKNOWN_ERROR
    statusAtFailure: Optional[TaskStatus] = None
    processExitCode: Optional[int] = None
