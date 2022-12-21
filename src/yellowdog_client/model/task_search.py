from dataclasses import dataclass
from typing import List, Optional

from .instant_range import InstantRange
from .sort_direction import SortDirection
from .task_status import TaskStatus


@dataclass
class TaskSearch:
    workRequirementId: Optional[str] = None
    taskGroupId: Optional[str] = None
    name: Optional[str] = None
    startedTime: Optional[InstantRange] = None
    finishedTime: Optional[InstantRange] = None
    hasInputs: Optional[bool] = None
    hasOutputs: Optional[bool] = None
    hasErrors: Optional[bool] = None
    tag: Optional[str] = None
    statuses: Optional[List[TaskStatus]] = None
    sortField: Optional[str] = None
    sortDirection: Optional[SortDirection] = None
