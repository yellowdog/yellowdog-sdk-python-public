from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class ComputeRequirementUsage:
    computeRequirementId: Optional[str] = None
    name: Optional[str] = None
    namespace: Optional[str] = None
    tag: Optional[str] = None
    createdById: Optional[str] = None
    createdTime: Optional[datetime] = None
    terminatedTime: Optional[datetime] = None
