from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from .compute_requirement_status import ComputeRequirementStatus
from .identified import Identified
from .tagged import Tagged


@dataclass
class ComputeRequirementSummary(Identified, Tagged):
    """Provides a summary of a ComputeRequirement including the ID that can be used to retrieve the full object."""
    id: Optional[str] = None
    namespace: Optional[str] = None
    """The user allocated namespace used to group compute requirements and other objects together."""
    name: Optional[str] = None
    """The user allocated name used to uniquely identify the compute requirement within its namespace."""
    tag: Optional[str] = None
    createdTime: Optional[datetime] = None
    status: Optional[ComputeRequirementStatus] = None
    """The status of the compute requirement."""
    aliveInstanceCount: int = 0
    """The number of alive computer machine instances in the compute requirement."""
    hasErroredSource: bool = False
    """Indicates if any of the compute provision sources is in ERRORED state."""
