from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

from .allowance import Allowance
from .allowance_limit_enforcement import AllowanceLimitEnforcement
from .allowance_reset_type import AllowanceResetType
from .instance_status import InstanceStatus


@dataclass
class RequirementsAllowance(Allowance):
    type: str = field(default="co.yellowdog.platform.model.RequirementsAllowance", init=False)
    id: Optional[str] = field(default=None, init=False)
    createdById: Optional[str] = field(default=None, init=False)
    remainingHours: Optional[float] = field(default=None, init=False)
    effectiveFrom: datetime
    resetType: AllowanceResetType
    limitEnforcement: AllowanceLimitEnforcement
    monitoredStatuses: List[InstanceStatus]
    requirementCreatedFromId: Optional[str] = None
    requirementCreatedById: Optional[str] = None
    namespace: Optional[str] = None
    tag: Optional[str] = None
    description: Optional[str] = None
    effectiveUntil: Optional[datetime] = None
    allowedHours: int = 0
    boostHours: Optional[int] = None
    resetInterval: Optional[int] = None
    hardLimitGraceMinutes: Optional[int] = None
