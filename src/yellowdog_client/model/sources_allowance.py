from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

from .allowance import Allowance
from .allowance_limit_enforcement import AllowanceLimitEnforcement
from .allowance_reset_type import AllowanceResetType
from .cloud_provider import CloudProvider
from .instance_status import InstanceStatus


@dataclass
class SourcesAllowance(Allowance):
    type: str = field(default="co.yellowdog.platform.model.SourcesAllowance", init=False)
    id: Optional[str] = field(default=None, init=False)
    createdById: Optional[str] = field(default=None, init=False)
    remainingHours: Optional[float] = field(default=None, init=False)
    effectiveFrom: datetime
    resetType: AllowanceResetType
    limitEnforcement: AllowanceLimitEnforcement
    monitoredStatuses: List[InstanceStatus]
    sourceCreatedFromId: Optional[str] = None
    provider: Optional[CloudProvider] = None
    regions: Optional[List[str]] = None
    instanceTypes: Optional[List[str]] = None
    credentialName: Optional[str] = None
    description: Optional[str] = None
    effectiveUntil: Optional[datetime] = None
    allowedHours: int = 0
    boostHours: Optional[int] = None
    resetInterval: Optional[int] = None
    hardLimitGraceMinutes: Optional[int] = None
