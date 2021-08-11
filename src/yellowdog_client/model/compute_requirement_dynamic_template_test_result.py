from dataclasses import dataclass, field
from typing import Optional

from .best_compute_source_report import BestComputeSourceReport
from .compute_requirement import ComputeRequirement
from .compute_requirement_template_test_result import ComputeRequirementTemplateTestResult


@dataclass
class ComputeRequirementDynamicTemplateTestResult(ComputeRequirementTemplateTestResult):
    type: str = field(default="co.yellowdog.platform.interaction.compute.ComputeRequirementDynamicTemplateTestResult", init=False)
    computeRequirement: Optional[ComputeRequirement] = None
    report: Optional[BestComputeSourceReport] = None
