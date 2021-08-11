from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional

from .identified import Identified
from .image_os_type import ImageOsType
from .machine_image import MachineImage
from .named import Named


@dataclass
class MachineImageGroup(Identified, Named):
    """Defines a group of functionally equivalent machine images across different provider/region environments."""
    id: Optional[str] = field(default=None, init=False)
    createdTime: Optional[datetime] = field(default=None, init=False)
    """The date and time when this machine image group was first created."""
    name: str
    """The user allocated name used to uniquely identify this machine image group within its family."""
    osType: ImageOsType
    """The operating system type of all images within this machine image group."""
    metadataSpecification: Optional[Dict[str, str]] = None
    """A map of user-definable key-value pairs used to specify metadata keys and, optionally, values required to be on all images within the machine image group."""
    images: Optional[List[MachineImage]] = None
    """A list of functionally equivalent machine images"""
