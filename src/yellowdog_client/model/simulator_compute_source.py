from dataclasses import dataclass, field
from typing import Dict, Optional, Set

from .cloud_provider import CloudProvider
from .compute_source import ComputeSource
from .compute_source_exhaustion import ComputeSourceExhaustion
from .compute_source_status import ComputeSourceStatus
from .compute_source_traits import ComputeSourceTraits
from .instance_summary import InstanceSummary


@dataclass
class SimulatorComputeSource(ComputeSource):
    """Defines a simulated source of compute that can be used to test the YellowDog Compute system."""
    type: str = field(default="co.yellowdog.platform.model.SimulatorComputeSource", init=False)
    traits: Optional[ComputeSourceTraits] = field(default=None, init=False)
    provider: Optional[CloudProvider] = field(default=None, init=False)
    subregion: Optional[str] = field(default=None, init=False)
    userData: Optional[str] = field(default=None, init=False)
    instanceTags: Optional[Dict[str, str]] = field(default=None, init=False)
    credentials: Optional[Set[str]] = field(default=None, init=False)
    id: Optional[str] = field(default=None, init=False)
    createdFromId: Optional[str] = field(default=None, init=False)
    instanceSummary: Optional[InstanceSummary] = field(default=None, init=False)
    status: Optional[ComputeSourceStatus] = field(default=None, init=False)
    statusMessage: Optional[str] = field(default=None, init=False)
    exhaustion: Optional[ComputeSourceExhaustion] = field(default=None, init=False)
    name: str
    credential: Optional[str] = None
    region: str = "sim-region"
    instanceType: str = "sim-instance"
    imageId: str = "sim-image"
    implicitCapacity: Optional[int] = None
    """The implicit capacity of this source that is not directly discoverable by the compute service, independent of limit."""
    instanceStartupTimeSeconds: int = 0
    """The simulated startup time for an instance."""
    instanceStartupTimeVariance: float = 0
    """A variance multiplier (from 0 to 1) applied randomly to the instance startup time."""
    instanceShutdownTimeSeconds: int = 0
    """The simulated shutdown time for an instance."""
    instanceShutdownTimeVariance: float = 0
    """A variance multiplier (from 0 to 1) applied randomly to the instance shutdown time."""
    unexpectedInstanceTerminationProbabilityPerSecond: float = 0
    """The probability (from 0 to 1) that any instance will be unexpectedly terminated in any given second."""
    limit: int = 0
