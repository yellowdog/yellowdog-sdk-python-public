from dataclasses import dataclass
from typing import Optional


@dataclass
class ComputeRequirementTemplateSummary:
    id: Optional[str] = None
    name: Optional[str] = None
    namespace: Optional[str] = None
    description: Optional[str] = None
    strategyType: Optional[str] = None
    type: Optional[str] = None
