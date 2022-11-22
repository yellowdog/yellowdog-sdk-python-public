from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional

from .identified import Identified
from .named import Named
from .run_specification import RunSpecification
from .tagged import Tagged
from .task_group_status import TaskGroupStatus
from .task_summary import TaskSummary


@dataclass
class TaskGroup(Identified, Named, Tagged):
    """Defines a group of tasks to be executed as part of a WorkRequirement."""
    id: Optional[str] = field(default=None, init=False)
    status: Optional[TaskGroupStatus] = field(default=None, init=False)
    """The task group status."""
    statusChangedTime: Optional[datetime] = field(default=None, init=False)
    """The date and time when the status last changed"""
    taskSummary: Optional[TaskSummary] = field(default=None, init=False)
    name: str
    """The user allocated name used to uniquely identify the task group within its work requirement."""
    runSpecification: RunSpecification
    """The run specification which determines the YellowDog Scheduler behaviours when it is executing the tasks within the task group."""
    tag: Optional[str] = None
    priority: float = 0
    """The task group priority."""
    dependentOn: Optional[str] = None
    """The name of another task group within the same WorkRequirement that must be successfully completed before the task group is started."""
    finishIfAllTasksFinished: bool = True
    """If true, the task group will finish automatically once all contained tasks are finished."""
    finishIfAnyTaskFailed: bool = False
    """If true, the task group will finish automatically if any contained tasks fail."""
    completedTaskTtl: Optional[timedelta] = None
    """The time to live for completed tasks. If set, tasks that have been completed for longer than this period will be deleted."""
