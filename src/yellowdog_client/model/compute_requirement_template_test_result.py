from abc import ABC
from typing import Optional

from .compute_requirement import ComputeRequirement



class ComputeRequirementTemplateTestResult(ABC):
    type: str
    computeRequirement: Optional[ComputeRequirement]
