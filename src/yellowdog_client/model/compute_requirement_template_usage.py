from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class ComputeRequirementTemplateUsage:
    templateId: str
    requirementName: str
    requirementNamespace: Optional[str] = None
    requirementTag: Optional[str] = None
    targetInstanceCount: int = 0
    imagesId: Optional[str] = None
    userData: Optional[str] = None
    instanceTags: Optional[Dict[str, str]] = None
    maintainInstanceCount: bool = False
