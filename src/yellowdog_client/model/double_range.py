from dataclasses import dataclass
from typing import Optional

from .range import Range


@dataclass
class DoubleRange(Range[float]):
    min: Optional[float] = None
    max: Optional[float] = None
