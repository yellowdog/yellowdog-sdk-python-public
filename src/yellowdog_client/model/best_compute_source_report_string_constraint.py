from dataclasses import dataclass, field
from typing import Optional, Set

from .best_compute_source_report_constraint import BestComputeSourceReportConstraint


@dataclass
class BestComputeSourceReportStringConstraint(BestComputeSourceReportConstraint):
    type: str = field(default="co.yellowdog.platform.model.BestComputeSourceReportStringConstraint", init=False)
    anyOf: Optional[Set[str]] = None
    noneOf: Optional[Set[str]] = None
    pattern: Optional[str] = None
