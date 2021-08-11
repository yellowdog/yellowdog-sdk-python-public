from dataclasses import dataclass
from typing import Optional


@dataclass
class NumericAttributeRange:
    min: Optional[float] = None
    max: Optional[float] = None
