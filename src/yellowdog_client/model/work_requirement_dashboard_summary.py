from dataclasses import dataclass
from typing import Dict, Optional

from .work_requirement_status import WorkRequirementStatus


@dataclass
class WorkRequirementDashboardSummary:
    statusCounts: Optional[Dict[WorkRequirementStatus, int]] = None
    errors: bool = False
