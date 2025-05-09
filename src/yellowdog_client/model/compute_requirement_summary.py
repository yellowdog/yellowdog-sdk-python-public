from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from .compute_requirement_status import ComputeRequirementStatus


@dataclass
class ComputeRequirementSummary:
    """Provides a summary of a ComputeRequirement including the ID that can be used to retrieve the full object."""
    id: Optional[str] = None
    """The ID of this compute requirement that is generated by YellowDog Compute when the requirement is first submitted."""
    namespace: Optional[str] = None
    """The user allocated namespace used to group compute requirements and other objects together."""
    name: Optional[str] = None
    """The user allocated name used to uniquely identify the compute requirement within its namespace."""
    tag: Optional[str] = None
    targetInstanceCount: int = 0
    """The number of instances to be provisioned to meet this compute requirement."""
    expectedInstanceCount: int = 0
    """The number of alive instances expected based on existing instances and the most recent provision action."""
    aliveInstanceCount: int = 0
    """The number of alive instances."""
    createdTime: Optional[datetime] = None
    """The date and time when this compute requirement was first submitted to YellowDog Compute."""
    status: Optional[ComputeRequirementStatus] = None
    """The status of this compute requirement."""
    healthy: bool = False
    """Represents whether the compute requirement is healthy or not. A compute requirement is considered healthy if no sources have a status of ERRORED"""
