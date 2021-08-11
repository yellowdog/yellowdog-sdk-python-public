from dataclasses import dataclass, field


@dataclass
class ComputeRequirementTemplateTestResult:
    type: str = field(default=None, init=False)
