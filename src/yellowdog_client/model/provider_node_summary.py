from dataclasses import dataclass
from typing import Optional

from .cloud_provider import CloudProvider


@dataclass
class ProviderNodeSummary:
    """A summary of a group of nodes."""
    provider: Optional[CloudProvider] = None
    totalNodes: Optional[int] = None
    workingNodes: Optional[int] = None
