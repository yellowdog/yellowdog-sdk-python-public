from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class MeasurementAggregate:
    metric: Optional[str] = None
    timestamp: Optional[datetime] = None
    averageValue: Optional[float] = None
