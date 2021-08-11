from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class BestComputeSourceReportSourceAttribute:
    value: Optional[Any] = None
    score: Optional[float] = None
    percentile: Optional[float] = None
