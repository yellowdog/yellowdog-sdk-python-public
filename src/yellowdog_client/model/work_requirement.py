from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

from .identified import Identified
from .named import Named
from .tagged import Tagged
from .task_group import TaskGroup
from .work_requirement_status import WorkRequirementStatus


@dataclass
class WorkRequirement(Identified, Named, Tagged):
    """
    Defines the requirement for work to be done with specifications on how it should be executed.

    This class is the main model object within the YellowDog Scheduler API.
    It is passed between the service and clients in order to request work to be done and to monitor the state of that work.
    """

    id: Optional[str] = field(default=None, init=False)
    """The ID of the work requirement that is generated by YellowDog Scheduler when the requirement is first submitted."""
    createdTime: Optional[datetime] = field(default=None, init=False)
    """The date and time when the work requirement was first submitted to YellowDog Scheduler."""
    status: Optional[WorkRequirementStatus] = field(default=None, init=False)
    """The status of the work requirement."""
    statusChangedTime: Optional[datetime] = field(default=None, init=False)
    """The date and time when the status last changed"""
    namespace: str
    """The user allocated namespace used to group work requirements and other objects together."""
    name: str
    """The user allocated name used to uniquely identify the work requirement within its namespace."""
    taskGroups: Optional[List[TaskGroup]] = None
    """The task groups containing tasks to be executed."""
    tag: Optional[str] = None
    priority: float = 0
    """The priority of the work requirement."""
