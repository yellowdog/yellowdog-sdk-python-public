from dataclasses import dataclass
from typing import Optional

from .cloud_provider import CloudProvider


@dataclass
class ComputeSourceTemplateSummary:
    id: Optional[str] = None
    name: Optional[str] = None
    namespace: Optional[str] = None
    description: Optional[str] = None
    sourceType: Optional[str] = None
    provider: Optional[CloudProvider] = None
