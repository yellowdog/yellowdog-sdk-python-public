from dataclasses import dataclass
from typing import Optional

from .allowance_limit_enforcement import AllowanceLimitEnforcement
from .instant_range import InstantRange
from .integer_range import IntegerRange
from .sort_direction import SortDirection


@dataclass
class AllowanceSearch:
    sortField: Optional[str] = None
    sortDirection: Optional[SortDirection] = None
    description: Optional[str] = None
    effectiveFrom: Optional[InstantRange] = None
    effectiveUntil: Optional[InstantRange] = None
    limitEnforcement: Optional[AllowanceLimitEnforcement] = None
    allowedHours: Optional[IntegerRange] = None
