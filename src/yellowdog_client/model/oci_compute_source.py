from abc import ABC
from typing import Dict, Optional

from .cloud_provider import CloudProvider
from .compute_source import ComputeSource
from .compute_source_exhaustion import ComputeSourceExhaustion
from .compute_source_status import ComputeSourceStatus
from .compute_source_traits import ComputeSourceTraits
from .instance_pricing import InstancePricing
from .instance_summary import InstanceSummary



class OciComputeSource(ComputeSource, ABC):
    """Derives from ComputeSource to provide the interface for all AWS compute source model objects."""
    type: str
    provider: Optional[CloudProvider]
    credential: Optional[str]
    compartmentId: Optional[str]
    """The OCI compartment ID (ocid) where instances will be provisioned."""
    availabilityDomain: Optional[str]
    """The OCI availability domain where instances will be provisioned."""
    subnetId: Optional[str]
    """The region-specific OCI Subnet ID (ocid) for the subnet to use for the provisioned instances."""
    shape: Optional[str]
    """The machine shape to use for the provisioned instances."""
    flexOcpus: Optional[float]
    """The number of OCPUs to provision on a flex type machine shape"""
    flexRam: Optional[float]
    """The amount of ram in GB to provision on a flex type machine shape"""
    sshKey: Optional[str]
    """The public SSH key. If provided, instances will be accessible with the matching private key through SSH."""
    instanceTags: Optional[Dict[str, str]]
    traits: Optional[ComputeSourceTraits]
    """Returns an object describing behavioural traits specific to this compute source."""
    instancePricing: Optional[InstancePricing]
    """Gets the instance pricing for this source, e.g. Spot"""
    id: Optional[str]
    createdFromId: Optional[str]
    """Gets the ID of the source template if this source was created from a template."""
    name: Optional[str]
    """Returns the name of this compute source (which must be unique within the containing ComputeRequirement)."""
    region: Optional[str]
    """Gets the provider-specific region where instances will be provisioned."""
    subregion: Optional[str]
    """Gets the provider-specific subregion (aka Availability Domain, Availability Zone or Zone) where instances will be provisioned."""
    instanceType: Optional[str]
    """Gets the provider-specific instance type of the instances that will be provisioned."""
    imageId: Optional[str]
    """Gets the image ID to use for the instances that will be provisioned."""
    userData: Optional[str]
    """Gets the user-data script to be passed to the provisioned instance at startup."""
    limit: Optional[int]
    """Returns the limit in number of instances that can be provisioned from this source."""
    instanceSummary: Optional[InstanceSummary]
    """A summary of instance counts according to instance status"""
    status: Optional[ComputeSourceStatus]
    """Gets the current provisioning status of this source."""
    statusMessage: Optional[str]
    """Gets the message associated with the current provisioning status of this source. Returns null if no further detail is relevant to the status."""
    exhaustion: Optional[ComputeSourceExhaustion]
    """If this source is associated with an exhausted allowance, gets the exhaustion state."""
    supportingResourceCreated: Optional[bool]
    """Indicates if supporting resources have been created for this source."""
