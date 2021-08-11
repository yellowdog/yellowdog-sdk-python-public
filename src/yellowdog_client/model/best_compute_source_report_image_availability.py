from dataclasses import dataclass
from typing import List, Optional

from .cloud_provider import CloudProvider


@dataclass
class BestComputeSourceReportImageAvailability:
    provider: Optional[CloudProvider] = None
    region: Optional[List[str]] = None
    supportedInstanceTypes: Optional[List[str]] = None
