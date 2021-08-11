from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from .identified import Identified
from .tagged import Tagged
from .work_requirement_status import WorkRequirementStatus


@dataclass
class WorkRequirementSummary(Identified, Tagged):
    """Provides a summary of a WorkRequirement including the ID that can be used to retrieve the full object."""
    id: Optional[str] = None
    namespace: Optional[str] = None
    """The user allocated namespace used to group work requirements and other objects together."""
    name: Optional[str] = None
    """The user allocated name used to uniquely identify the work requirement within its namespace."""
    tag: Optional[str] = None
    createdTime: Optional[datetime] = None
    """The date and time when the work requirement was first submitted to YellowDog Scheduler."""
    priority: float = 0
    """The priority of the work requirement."""
    completedTaskCount: int = 0
    """The count of successfully completed tasks in the work requirement."""
    totalTaskCount: int = 0
    """The total count of tasks in the work requirement."""
    status: Optional[WorkRequirementStatus] = None
    """The status of the work requirement."""
    healthy: bool = False
    """Indicates if the work requirement is healthy. If false then tasks may have failed or task groups may be starved."""
