from dataclasses import dataclass, field
from typing import Dict, List, Optional

from .compute_requirement_template import ComputeRequirementTemplate
from .compute_source_usage import ComputeSourceUsage


@dataclass
class ComputeRequirementStaticTemplate(ComputeRequirementTemplate):
    type: str = field(default="co.yellowdog.platform.model.ComputeRequirementStaticTemplate", init=False)
    id: Optional[str] = field(default=None, init=False)
    name: str
    strategyType: str
    sources: List[ComputeSourceUsage]
    namespace: Optional[str] = None
    description: Optional[str] = None
    imagesId: Optional[str] = None
    userData: Optional[str] = None
    instanceTags: Optional[Dict[str, str]] = None
