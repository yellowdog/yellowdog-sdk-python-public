from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional

from .cloud_provider import CloudProvider
from .identified import Identified
from .image_os_type import ImageOsType
from .named import Named


@dataclass
class MachineImage(Identified, Named):
    """Describes a machine software image, its capabilities and where it is available."""
    id: Optional[str] = field(default=None, init=False)
    createdTime: Optional[datetime] = field(default=None, init=False)
    """The date and time when this machine image record was first created. NB: This may not be indicative of the time the actual image was created."""
    name: str
    """The machine image name"""
    provider: CloudProvider
    """The compute provider in whose system the image is registered."""
    providerImageId: str
    """The ID for the image in the compute provider's system."""
    osType: ImageOsType
    """The image operating system type"""
    regions: Optional[List[str]] = None
    """The regions in which the image is registered. If null or empty then the image is assumed to be available in all regions."""
    supportedInstanceTypes: Optional[List[str]] = None
    """The instance types that can be used with the image in the cloud provider's system. If null or empty then the image is assumed to compatible with any instance type."""
    metadata: Optional[Dict[str, str]] = None
    """A map of user-definable key-value pairs to hold extra metadata properties related to the machine image."""
