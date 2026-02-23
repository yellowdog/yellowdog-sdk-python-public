from abc import ABC
from datetime import datetime
from typing import Optional

from .cloud_provider import CloudProvider
from .instance_id import InstanceId
from .instance_status import InstanceStatus



class Instance(ABC):
    """
    Describes an instance provisioned for a compute requirement.

    This class provides common fields shared across all compute provisioners.
    It is generally specialised for each provisioner to add extra fields specific to that provisioner.
    """

    type: str
    id: Optional[InstanceId]
    """The unique identifier for this instance formed from the YellowDog Compute Source ID and the provider supplied instance ID"""
    createdTime: Optional[datetime]
    """The date and time when this instance was first created."""
    provider: Optional[CloudProvider]
    """The cloud provider that supplies this instance."""
    instanceType: Optional[str]
    """The machine type of this instance."""
    region: Optional[str]
    """The region where this instance is provisioned."""
    subregion: Optional[str]
    """The subregion where this instance is provisioned."""
    imageId: Optional[str]
    """The machine image ID used for this instance."""
    hostname: Optional[str]
    """The hostname of this instance."""
    privateIpAddress: Optional[str]
    """The private IP address of this instance."""
    publicIpAddress: Optional[str]
    """The public IP address of this instance."""
    spot: bool
    """Indicates if this instance was provisioned via spot pricing vs on-demand."""
    status: Optional[InstanceStatus]
    """The status of this instance."""
    statusChangedTime: Optional[datetime]
    """The date and time when the status last changed"""
