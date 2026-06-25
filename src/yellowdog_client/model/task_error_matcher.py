from dataclasses import dataclass
from typing import List, Optional

from .task_status import TaskStatus


@dataclass
class TaskErrorMatcher:
    """
    .. deprecated:: (unknown)
        Use :class:`RetryPolicy` instead
    """

    errorTypes: Optional[List[str]] = None
    statusesAtFailure: Optional[List[TaskStatus]] = None
    processExitCodes: Optional[List[int]] = None
