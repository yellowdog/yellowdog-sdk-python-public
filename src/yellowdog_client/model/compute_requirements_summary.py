from dataclasses import dataclass
from typing import Dict, Optional

from .compute_requirement_status import ComputeRequirementStatus


@dataclass
class ComputeRequirementsSummary:
    statusCounts: Optional[Dict[ComputeRequirementStatus, int]] = None
    errors: bool = False
