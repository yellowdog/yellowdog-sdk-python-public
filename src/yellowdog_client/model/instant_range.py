from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from .range import Range


@dataclass
class InstantRange(Range):
    min: Optional[datetime] = None
    max: Optional[datetime] = None
