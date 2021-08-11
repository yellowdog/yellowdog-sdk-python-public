from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from .identified import Identified
from .image_access import ImageAccess
from .image_os_type import ImageOsType


@dataclass
class MachineImageFamilySummary(Identified):
    """Provides a summary of a Machine Image Family including the ID that can be used to retrieve the full object."""
    id: Optional[str] = None
    namespace: Optional[str] = None
    """The user allocated namespace used to group machine image families and other objects together."""
    name: Optional[str] = None
    """The user allocated name used to uniquely identify the machine image family within its namespace."""
    createdTime: Optional[datetime] = None
    """The date and time when the machine image family was first created."""
    access: Optional[ImageAccess] = None
    """The access level for this machine image family and any contained groups and images."""
    osType: Optional[ImageOsType] = None
    """The operating system type of all images within this machine image family."""
    owned: Optional[bool] = None
    """Indicates if the machine image family is owned by the authenticated account."""
