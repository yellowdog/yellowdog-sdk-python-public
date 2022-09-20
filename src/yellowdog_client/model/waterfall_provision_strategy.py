from dataclasses import dataclass, field
from typing import List, Optional, Set

from .compute_provision_strategy import ComputeProvisionStrategy
from .compute_source import ComputeSource


@dataclass
class WaterfallProvisionStrategy(ComputeProvisionStrategy):
    """
    Instructs YellowDog Compute to provision instances by acquiring the maximum available from each compute source in order,
    until the required number of instances is reached.
    """

    type: str = field(default="co.yellowdog.platform.model.WaterfallProvisionStrategy", init=False)
    credentials: Optional[Set[str]] = field(default=None, init=False)
    sources: List[ComputeSource]
    """The compute sources to use for the compute requirement."""
