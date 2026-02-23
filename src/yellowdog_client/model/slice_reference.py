from dataclasses import dataclass
from typing import ClassVar, Optional


@dataclass
class SliceReference:
    MAX_SIZE: ClassVar[int] = 1000
    MIN_SIZE: ClassVar[int] = 1
    sliceId: Optional[str] = None
    size: Optional[int] = None
