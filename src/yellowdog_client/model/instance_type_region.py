from dataclasses import dataclass
from typing import List, Optional


@dataclass
class InstanceTypeRegion:
    name: Optional[str] = None
    subRegions: Optional[List[str]] = None
