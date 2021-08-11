from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Optional

from .task_status import TaskStatus


@dataclass
class TaskSummary:
    statusCounts: Optional[Dict[TaskStatus, int]] = None
    taskCount: int = 0
    lastUpdatedTime: Optional[datetime] = None
