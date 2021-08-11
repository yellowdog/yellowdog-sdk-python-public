from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class BestComputeSourceReportPreference:
    weight: Optional[float] = None
    lowestValue: Optional[Any] = None
    highestValue: Optional[Any] = None
