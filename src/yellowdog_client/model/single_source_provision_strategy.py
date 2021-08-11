from dataclasses import dataclass, field
from typing import List, Optional, Set

from .compute_provision_strategy import ComputeProvisionStrategy
from .compute_source import ComputeSource


@dataclass
class SingleSourceProvisionStrategy(ComputeProvisionStrategy):
    """Instructs YellowDog Compute to use a single compute source for the compute requirement."""
    type: str = field(default="co.yellowdog.platform.model.SingleSourceProvisionStrategy", init=False)
    credentials: Optional[Set[str]] = field(default=None, init=False)
    sources: List[ComputeSource]
    """The compute sources to use for the compute requirement."""
