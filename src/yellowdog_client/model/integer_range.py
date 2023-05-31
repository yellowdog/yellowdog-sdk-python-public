from dataclasses import dataclass
from typing import Optional

from .range import Range


@dataclass
class IntegerRange(Range):
    min: Optional[int] = None
    max: Optional[int] = None
