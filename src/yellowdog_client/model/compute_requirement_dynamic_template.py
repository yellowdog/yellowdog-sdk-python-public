from dataclasses import dataclass, field
from typing import Dict, List, Optional

from .attribute_constraint import AttributeConstraint
from .attribute_preference import AttributePreference
from .compute_requirement_template import ComputeRequirementTemplate
from .compute_source_traits_filter import ComputeSourceTraitsFilter


@dataclass
class ComputeRequirementDynamicTemplate(ComputeRequirementTemplate):
    type: str = field(default="co.yellowdog.platform.model.ComputeRequirementDynamicTemplate", init=False)
    id: Optional[str] = field(default=None, init=False)
    name: str
    strategyType: str
    namespace: Optional[str] = None
    description: Optional[str] = None
    minimumSourceCount: Optional[int] = None
    maximumSourceCount: Optional[int] = None
    imagesId: Optional[str] = None
    userData: Optional[str] = None
    instanceTags: Optional[Dict[str, str]] = None
    constraints: Optional[List[AttributeConstraint]] = None
    preferences: Optional[List[AttributePreference]] = None
    sourceTraits: Optional[ComputeSourceTraitsFilter] = None
