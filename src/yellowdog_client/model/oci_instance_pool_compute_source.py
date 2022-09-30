from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Optional, Set

from .compute_source_exhaustion_status import ComputeSourceExhaustionStatus
from .compute_source_status import ComputeSourceStatus
from .compute_source_traits import ComputeSourceTraits
from .oci_compute_source import OciComputeSource


@dataclass
class OciInstancePoolComputeSource(OciComputeSource):
    """Defines a source of compute composed of OCI instances provisioned using the OCI Instance Pool API."""
    type: str = field(default="co.yellowdog.platform.model.OciInstancePoolComputeSource", init=False)
    traits: Optional[ComputeSourceTraits] = field(default=None, init=False)
    credentials: Optional[Set[str]] = field(default=None, init=False)
    id: Optional[str] = field(default=None, init=False)
    createdFromId: Optional[str] = field(default=None, init=False)
    clusterNetworkId: Optional[str] = field(default=None, init=False)
    """The OCID of the Cluster Network if used."""
    instancePoolId: Optional[str] = field(default=None, init=False)
    """The OCID of the instance pool in which instances are started."""
    requestedInstanceCount: Optional[int] = field(default=None, init=False)
    expectedInstanceCount: Optional[int] = field(default=None, init=False)
    status: Optional[ComputeSourceStatus] = field(default=None, init=False)
    statusMessage: Optional[str] = field(default=None, init=False)
    exhaustionStatus: Optional[ComputeSourceExhaustionStatus] = field(default=None, init=False)
    expectedExhaustionTermination: Optional[datetime] = field(default=None, init=False)
    name: str
    credential: str
    region: str
    """The OCI region where instances will be provisioned."""
    compartmentId: str
    """The OCI compartment ID (ocid) where instances will be provisioned."""
    imageId: str
    """The region-specific OCI Image ID (ocid) for the image to use for the provisioned instances."""
    shape: str
    subnetId: str
    """The region-specific OCI Subnet ID (ocid) for the subnet to use for the provisioned instances."""
    sshKey: Optional[str] = None
    """The public SSH key. If provided, instances will be accessible with the matching private key through SSH."""
    availabilityDomain: Optional[str] = None
    """The OCI availability domain where instances will be provisioned."""
    flexOcpus: Optional[float] = None
    flexRam: Optional[float] = None
    limit: int = 0
    assignPublicIp: bool = False
    """Indicates if provisioned instances should be assigned public IP addresses."""
    createClusterNetwork: Optional[bool] = None
    userData: Optional[str] = None
    instanceTags: Optional[Dict[str, str]] = None
