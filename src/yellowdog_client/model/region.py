from dataclasses import dataclass
from typing import Optional

from .cloud_provider import CloudProvider


@dataclass
class Region:
    provider: Optional[CloudProvider] = None
    name: Optional[str] = None
