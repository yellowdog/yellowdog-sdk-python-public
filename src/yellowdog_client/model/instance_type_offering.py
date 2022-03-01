from dataclasses import dataclass
from typing import Optional

from .cloud_provider import CloudProvider


@dataclass
class InstanceTypeOffering:
    provider: Optional[CloudProvider] = None
    region: Optional[str] = None
    subRegion: Optional[str] = None
    instanceType: Optional[str] = None
