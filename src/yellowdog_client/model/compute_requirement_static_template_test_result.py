from dataclasses import dataclass, field
from typing import Optional

from .compute_requirement import ComputeRequirement
from .compute_requirement_template_test_result import ComputeRequirementTemplateTestResult


@dataclass
class ComputeRequirementStaticTemplateTestResult(ComputeRequirementTemplateTestResult):
    type: str = field(default="co.yellowdog.platform.interaction.compute.ComputeRequirementStaticTemplateTestResult", init=False)
    computeRequirement: Optional[ComputeRequirement] = None
