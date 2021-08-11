from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional

from .identified import Identified
from .image_access import ImageAccess
from .image_os_type import ImageOsType
from .machine_image_group import MachineImageGroup
from .named import Named


@dataclass
class MachineImageFamily(Identified, Named):
    """Defines a family of versions of machine image groups."""
    id: Optional[str] = field(default=None, init=False)
    createdTime: Optional[datetime] = field(default=None, init=False)
    """The date and time when this machine image family was first created."""
    namespace: str
    """The user allocated namespace used to group machine image families and other objects together."""
    name: str
    """The user allocated name used to uniquely identify this machine image family within its namespace."""
    osType: ImageOsType
    """The operating system type of all images within this machine image family."""
    access: ImageAccess = ImageAccess.PRIVATE
    """The access level for this machine image family and any contained groups and images."""
    metadataSpecification: Optional[Dict[str, str]] = None
    """A map of user-definable key-value pairs used to specify metadata keys and, optionally, values required to be on all images within the machine image family."""
    imageGroups: Optional[List[MachineImageGroup]] = None
    """A list of the related machine image groups."""
