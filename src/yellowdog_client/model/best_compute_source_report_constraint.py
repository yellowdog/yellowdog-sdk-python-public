from dataclasses import dataclass, field


@dataclass
class BestComputeSourceReportConstraint:
    type: str = field(default=None, init=False)
