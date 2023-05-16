from dataclasses import dataclass, field
from typing import Dict, Optional, Set

from .compute_source_exhaustion import ComputeSourceExhaustion
from .compute_source_status import ComputeSourceStatus
from .compute_source_traits import ComputeSourceTraits
from .gce_compute_source import GceComputeSource
from .instance_summary import InstanceSummary


@dataclass
class GceInstancesComputeSource(GceComputeSource):
    """Defines a source of compute composed of Google Compute Engine (GCE) instances individually provisioned."""
    type: str = field(default="co.yellowdog.platform.model.GceInstancesComputeSource", init=False)
    traits: Optional[ComputeSourceTraits] = field(default=None, init=False)
    credentials: Optional[Set[str]] = field(default=None, init=False)
    id: Optional[str] = field(default=None, init=False)
    createdFromId: Optional[str] = field(default=None, init=False)
    instanceSummary: Optional[InstanceSummary] = field(default=None, init=False)
    status: Optional[ComputeSourceStatus] = field(default=None, init=False)
    statusMessage: Optional[str] = field(default=None, init=False)
    exhaustion: Optional[ComputeSourceExhaustion] = field(default=None, init=False)
    name: str
    credential: str
    project: str
    region: str
    machineType: str
    image: str
    limit: int = 0
    assignPublicIp: bool = False
    """Indicates if provisioned instances should be assigned public IP addresses."""
    specifyMinimum: bool = False
    """
    Indicates if YellowDog Compute should specify the minimum when requesting instances. NB: This can only be used with a limit set between 1..1000
    If true, then no instances are provisioned unless all requested instances are available;
    otherwise, if false, YellowDog Compute will provision as many instances as possible up to the number requested from this compute source.
    """

    createCompactPlacementPolicy: Optional[bool] = None
    """Indicates if instances should be provisioned using a compact placement policy."""
    userData: Optional[str] = None
    instanceTags: Optional[Dict[str, str]] = None
    sshKeys: Optional[str] = None
    """A list of public SSH keys. If provided, instances will be accessible with the matching private keys through SSH."""
    zone: Optional[str] = None
    network: Optional[str] = None
    subnetwork: Optional[str] = None
    preemptible: bool = False
    spot: bool = False
    confidential: bool = False
    acceleratorType: Optional[str] = None
    acceleratorCount: int = 0
