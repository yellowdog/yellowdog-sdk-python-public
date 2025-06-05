from dataclasses import dataclass
from typing import List, Optional

from .task_status import TaskStatus


@dataclass
class TaskErrorMatcher:
    errorTypes: Optional[List[str]] = None
    statusesAtFailure: Optional[List[TaskStatus]] = None
    processExitCodes: Optional[List[int]] = None
