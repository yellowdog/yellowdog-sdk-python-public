from dataclasses import dataclass, field
from typing import Dict, Optional, Set

from .cloud_provider import CloudProvider
from .compute_source_exhaustion import ComputeSourceExhaustion
from .compute_source_status import ComputeSourceStatus
from .compute_source_traits import ComputeSourceTraits
from .instance_pricing import InstancePricing
from .instance_summary import InstanceSummary
from .oci_compute_source import OciComputeSource


@dataclass
class OciInstancePoolComputeSource(OciComputeSource):
    """Defines a source of compute composed of OCI instances provisioned using the OCI Instance Pool API."""
    type: str = field(default="co.yellowdog.platform.model.OciInstancePoolComputeSource", init=False)
    traits: Optional[ComputeSourceTraits] = field(default=None, init=False)
    instancePricing: Optional[InstancePricing] = field(default=None, init=False)
    credentials: Optional[Set[str]] = field(default=None, init=False)
    id: Optional[str] = field(default=None, init=False)
    createdFromId: Optional[str] = field(default=None, init=False)
    instanceSummary: Optional[InstanceSummary] = field(default=None, init=False)
    status: Optional[ComputeSourceStatus] = field(default=None, init=False)
    statusMessage: Optional[str] = field(default=None, init=False)
    exhaustion: Optional[ComputeSourceExhaustion] = field(default=None, init=False)
    supportingResourceCreated: Optional[bool] = field(default=None, init=False)
    provider: Optional[CloudProvider] = field(default=None, init=False)
    name: str
    credential: str
    region: str
    """The OCI region where instances will be provisioned."""
    compartmentId: str
    """The OCI compartment ID (ocid) where instances will be provisioned."""
    imageId: str
    """
    The region-specific OCI Image ID (ocid) for the image to use for the provisioned instances.
    In a compute source template, this may instead be the ID of a :class:`MachineImage`, :class:`MachineImageGroup` or :class:`MachineImageFamily`,
    resolved to a matching OCI Image ID (ocid) when a compute requirement is provisioned from the template,
    or "*" for the image to be supplied by the compute requirement template or when provisioning from it.
    A value in a compute source template is not checked until a compute requirement is provisioned from it.
    """

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
    bootVolumeSizeGb: Optional[int] = None
