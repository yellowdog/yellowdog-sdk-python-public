from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from .cloud_provider import CloudProvider
from .instance import Instance
from .instance_id import InstanceId
from .instance_status import InstanceStatus


@dataclass
class AlibabaInstance(Instance):
    """Extends Instance to add fields specific to the Alibaba Cloud compute sources."""
    type: str = field(default="co.yellowdog.platform.model.AlibabaInstance", init=False)
    id: Optional[InstanceId] = None
    """The unique identifier for this instance formed from the YellowDog Compute Source ID and the provider supplied instance ID"""
    createdTime: Optional[datetime] = None
    """The date and time when this instance was first created."""
    provider: Optional[CloudProvider] = None
    """The cloud provider that supplies this instance."""
    instanceType: Optional[str] = None
    """The machine type of this instance."""
    region: Optional[str] = None
    """The region where this instance is provisioned."""
    subregion: Optional[str] = None
    """The subregion where this instance is provisioned."""
    imageId: Optional[str] = None
    """The machine image ID used for this instance."""
    hostname: Optional[str] = None
    """The hostname of this instance."""
    privateIpAddress: Optional[str] = None
    """The private IP address of this instance."""
    publicIpAddress: Optional[str] = None
    """The public IP address of this instance."""
    spot: bool = False
    """Indicates if this instance was provisioned via spot pricing vs on-demand."""
    status: Optional[InstanceStatus] = None
    """The status of this instance."""
    statusChangedTime: Optional[datetime] = None
    """The date and time when the status last changed"""
