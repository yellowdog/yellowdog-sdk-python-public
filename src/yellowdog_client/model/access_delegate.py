from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Set

from .identified import Identified
from .permission import Permission


@dataclass
class AccessDelegate(Identified):
    """Represents a user or application delegate within the YellowDog Platform."""
    id: Optional[str] = field(default=None, init=False)
    creator: Optional[str] = None
    subject: Optional[str] = None
    description: Optional[str] = None
    createdTime: Optional[datetime] = None
    requiredPermissions: Optional[Set[Permission]] = None
