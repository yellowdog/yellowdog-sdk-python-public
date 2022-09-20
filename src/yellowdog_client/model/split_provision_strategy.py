from dataclasses import dataclass, field
from typing import List, Optional, Set

from .compute_provision_strategy import ComputeProvisionStrategy
from .compute_source import ComputeSource


@dataclass
class SplitProvisionStrategy(ComputeProvisionStrategy):
    """Instructs YellowDog Compute to split the provision of instances as evenly as possible across the compute sources."""
    type: str = field(default="co.yellowdog.platform.model.SplitProvisionStrategy", init=False)
    credentials: Optional[Set[str]] = field(default=None, init=False)
    sources: List[ComputeSource]
    """The compute sources to use for the compute requirement."""
