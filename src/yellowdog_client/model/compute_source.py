from abc import ABC
from typing import ClassVar, Dict, Optional

from .cloud_provider import CloudProvider
from .compute_source_exhaustion import ComputeSourceExhaustion
from .compute_source_status import ComputeSourceStatus
from .compute_source_traits import ComputeSourceTraits
from .identified import Identified
from .instance_pricing import InstancePricing
from .instance_summary import InstanceSummary
from .named import Named



class ComputeSource(Identified, Named, ABC):
    """
    The interface implemented by all compute source model objects.

    A compute source describes a specific source for acquiring instances in order to meet the compute requirement.
    """

    DEFAULT_ASSIGN_PUBLIC_IP: ClassVar[bool] = False
    type: str
    traits: Optional[ComputeSourceTraits]
    """Returns an object describing behavioural traits specific to this compute source."""
    provider: Optional[CloudProvider]
    """Gets the Cloud Provider for this source."""
    instancePricing: Optional[InstancePricing]
    """Gets the instance pricing for this source, e.g. Spot"""
    id: Optional[str]
    createdFromId: Optional[str]
    """Gets the ID of the source template if this source was created from a template."""
    name: Optional[str]
    """Returns the name of this compute source (which must be unique within the containing ComputeRequirement)."""
    credential: Optional[str]
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
    instanceTags: Optional[Dict[str, str]]
    """Gets the custom instance tags to be set on the provisioned instance at startup."""
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
