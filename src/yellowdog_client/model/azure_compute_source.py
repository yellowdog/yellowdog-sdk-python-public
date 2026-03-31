from abc import ABC
from typing import Dict, Optional

from .cloud_provider import CloudProvider
from .compute_source import ComputeSource
from .compute_source_exhaustion import ComputeSourceExhaustion
from .compute_source_status import ComputeSourceStatus
from .compute_source_traits import ComputeSourceTraits
from .instance_pricing import InstancePricing
from .instance_summary import InstanceSummary



class AzureComputeSource(ComputeSource, ABC):
    """Derives from :class:`ComputeSource` to provide the interface for all Azure compute source model objects."""
    type: str
    provider: Optional[CloudProvider]
    instancePricing: Optional[InstancePricing]
    credential: Optional[str]
    availabilityZone: Optional[str]
    networkResourceGroupName: Optional[str]
    networkName: Optional[str]
    subnetName: Optional[str]
    environment: Optional[str]
    """
    Allows the specification of an Azure environment other than the default public environment.
    This should normally be left blank.
    Valid values are "china", "germany", "us_government".
    """

    vmSize: Optional[str]
    adminUserCredential: Optional[str]
    sshKey: Optional[str]
    createProximityPlacementGroup: Optional[bool]
    useAcceleratedNetworking: Optional[bool]
    useSpot: Optional[bool]
    """Indicates if Spot VMs should be requested from Azure. Requires Spot max price to be set."""
    spotMaxPrice: Optional[float]
    """The maximum price that will be paid for Spot VMs provisioned from this source."""
    supportingResourceCreated: Optional[bool]
    instanceTags: Optional[Dict[str, str]]
    traits: Optional[ComputeSourceTraits]
    """Returns an object describing behavioural traits specific to this compute source."""
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
