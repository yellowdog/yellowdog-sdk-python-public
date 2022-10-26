from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class TaskError:
    """Holds details of an error that occurred during execution of the task."""
    timestamp: Optional[datetime] = None
    """The time at which the error occurred."""
    workerId: Optional[str] = None
    """The ID of the worker where the error occurred."""
    error: Optional[str] = None
    """A description of the error."""
