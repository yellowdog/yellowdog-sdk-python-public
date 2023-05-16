from dataclasses import dataclass, field
from typing import Dict, Optional, Set

from .azure_compute_source import AzureComputeSource
from .compute_source_exhaustion import ComputeSourceExhaustion
from .compute_source_status import ComputeSourceStatus
from .compute_source_traits import ComputeSourceTraits
from .instance_summary import InstanceSummary


@dataclass
class AzureScaleSetComputeSource(AzureComputeSource):
    type: str = field(default="co.yellowdog.platform.model.AzureScaleSetComputeSource", init=False)
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
    region: str
    """The Azure region where instances will be provisioned."""
    networkResourceGroupName: str
    networkName: str
    subnetName: str
    vmSize: str
    imageId: str
    """The YellowDog prefixed Azure image ID for the image to use for the provisioned instances."""
    availabilityZone: Optional[str] = None
    environment: Optional[str] = None
    userData: Optional[str] = None
    instanceTags: Optional[Dict[str, str]] = None
    adminUserCredential: Optional[str] = None
    """
    Optionally specifies the name of an AzureInstanceCredential that provides the admin user name and password to use for root (Linux) or administrator (Windows).
    If not specified, then YellowDog Compute uses the default admin user name and a different randomly generated password for each instance.
    """

    sshKey: Optional[str] = None
    """The public SSH key. If provided, instances will be accessible with the matching private key through SSH."""
    assignPublicIp: bool = False
    createProximityPlacementGroup: Optional[bool] = None
    """Indicates if instances should be provisioned within a proximity placement group."""
    useAcceleratedNetworking: Optional[bool] = None
    useSpot: Optional[bool] = None
    spotMaxPrice: Optional[float] = None
    limit: int = 0
