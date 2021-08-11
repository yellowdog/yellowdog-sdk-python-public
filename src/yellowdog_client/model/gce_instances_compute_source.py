from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Set

from .compute_source_exhaustion_status import ComputeSourceExhaustionStatus
from .compute_source_status import ComputeSourceStatus
from .compute_source_traits import ComputeSourceTraits
from .gce_compute_source import GceComputeSource


@dataclass
class GceInstancesComputeSource(GceComputeSource):
    """Defines a source of compute composed of Google Compute Engine (GCE) instances individually provisioned."""
    type: str = field(default="co.yellowdog.platform.model.GceInstancesComputeSource", init=False)
    traits: Optional[ComputeSourceTraits] = field(default=None, init=False)
    credentials: Optional[Set[str]] = field(default=None, init=False)
    id: Optional[str] = field(default=None, init=False)
    createdFromId: Optional[str] = field(default=None, init=False)
    status: Optional[ComputeSourceStatus] = field(default=None, init=False)
    statusMessage: Optional[str] = field(default=None, init=False)
    exhaustionStatus: Optional[ComputeSourceExhaustionStatus] = field(default=None, init=False)
    expectedExhaustionTermination: Optional[datetime] = field(default=None, init=False)
    name: str
    credential: str
    project: str
    region: str
    zone: str
    machineType: str
    image: str
    limit: int = 0
    assignPublicIp: bool = True
    """Indicates if provisioned instances should be assigned public IP addresses."""
    userData: Optional[str] = None
    """The user-data script to be passed to the provisioned instance at startup."""
    sshKeys: Optional[str] = None
    """A list of public SSH keys. If provided, instances will be accessible with the matching private keys through SSH."""
    network: Optional[str] = None
    subnetwork: Optional[str] = None
    preemptible: bool = False
    acceleratorType: Optional[str] = None
    acceleratorCount: int = 0
