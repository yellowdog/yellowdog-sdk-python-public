from dataclasses import dataclass
from typing import Optional

from .work_requirement_status import WorkRequirementStatus


@dataclass
class WorkRequirementStatusCount:
    errored: bool = False
    status: Optional[WorkRequirementStatus] = None
    count: int = 0
