from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from .cloud_provider import CloudProvider
from .instance import Instance
from .instance_status import InstanceStatus


@dataclass
class GceInstance(Instance):
    """Extends Instance to add fields specific to the Google Compute Engine (GCE) compute source."""
    type: str = field(default="co.yellowdog.platform.model.GceInstance", init=False)
    id: Optional[str] = field(default=None, init=False)
    """The ID of this instance."""
    preemptible: bool = False
    confidential: bool = False
    createdTime: Optional[datetime] = None
    """The date and time when this instance was first created."""
    removedTime: Optional[datetime] = None
    """The date and time when this instance was recognized to no longer be utilized by the provider."""
    sourceId: Optional[str] = None
    """The ID of the compute source from which this instance was provisioned."""
    imageId: Optional[str] = None
    """The machine image ID used for this instance."""
    instanceType: Optional[str] = None
    """The machine type of this instance."""
    provider: Optional[CloudProvider] = None
    """The cloud provider that supplies this instance."""
    region: Optional[str] = None
    """The region where this instance is provisioned."""
    status: Optional[InstanceStatus] = None
    """The status of this instance."""
    subregion: Optional[str] = None
    """The subregion where this instance is provisioned."""
    privateIpAddress: Optional[str] = None
    """The private IP address of this instance."""
    publicIpAddress: Optional[str] = None
    """The public IP address of this instance."""
    hostname: Optional[str] = None
    """The hostname of this instance."""
    spot: bool = False
    """Indicates if this instance was provisioned via spot pricing vs on-demand."""
