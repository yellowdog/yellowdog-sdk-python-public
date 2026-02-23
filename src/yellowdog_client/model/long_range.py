from dataclasses import dataclass
from typing import Optional

from .range import Range


@dataclass
class LongRange(Range[int]):
    min: Optional[int] = None
    max: Optional[int] = None
