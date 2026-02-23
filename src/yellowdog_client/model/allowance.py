from abc import ABC
from datetime import datetime
from typing import ClassVar, List, Optional

from .allowance_limit_enforcement import AllowanceLimitEnforcement
from .allowance_reset_type import AllowanceResetType
from .identified import Identified
from .instance_status import InstanceStatus



class Allowance(Identified, ABC):
    DESCRIPTION_MAX_LENGTH: ClassVar[int] = 100
    type: str
    id: Optional[str]
    description: Optional[str]
    createdById: Optional[str]
    effectiveFrom: datetime
    effectiveUntil: Optional[datetime]
    allowedHours: int
    remainingHours: Optional[float]
    boostHours: Optional[int]
    resetType: AllowanceResetType
    resetInterval: Optional[int]
    limitEnforcement: AllowanceLimitEnforcement
    hardLimitGraceMinutes: Optional[int]
    monitoredStatuses: List[InstanceStatus]
