from dataclasses import dataclass
from typing import Optional


@dataclass
class SliceReference:
    sliceId: Optional[str] = None
    size: Optional[int] = None
