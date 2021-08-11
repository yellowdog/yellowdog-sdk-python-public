from dataclasses import dataclass, field
from typing import Optional

from .best_compute_source_report_constraint import BestComputeSourceReportConstraint


@dataclass
class BestComputeSourceReportNumericConstraint(BestComputeSourceReportConstraint):
    type: str = field(default="co.yellowdog.platform.model.BestComputeSourceReportNumericConstraint", init=False)
    min: Optional[float] = None
    max: Optional[float] = None
