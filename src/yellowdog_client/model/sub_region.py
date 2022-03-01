from dataclasses import dataclass
from typing import Optional

from .cloud_provider import CloudProvider


@dataclass
class SubRegion:
    provider: Optional[CloudProvider] = None
    region: Optional[str] = None
    name: Optional[str] = None
