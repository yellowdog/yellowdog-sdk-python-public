from dataclasses import dataclass
from typing import Optional


@dataclass
class ComputeSourceTraitsFilter:
    canStopStart: Optional[bool] = None
    canScaleOut: Optional[bool] = None
    isSelfMaintained: Optional[bool] = None
