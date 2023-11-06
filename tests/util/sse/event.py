from dataclasses import dataclass
from typing import Optional


@dataclass
class Event:
    type: Optional[str] = None
    data: Optional[str] = None
    id: Optional[str] = None
    retry: Optional[int] = None
