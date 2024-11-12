from dataclasses import dataclass
from typing import Optional


@dataclass
class ProviderRegionNodeSummary:
    """A summary of a group of nodes."""
    region: Optional[str] = None
    totalNodes: Optional[int] = None
    workingNodes: Optional[int] = None
