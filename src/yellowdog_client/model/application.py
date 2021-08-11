from dataclasses import dataclass, field
from typing import List, Optional

from .access_delegate import AccessDelegate
from .identified import Identified
from .named import Named


@dataclass
class Application(Identified, Named):
    """Represents a user application within the YellowDog Platform."""
    id: Optional[str] = field(default=None, init=False)
    name: str
    createdByUserId: str
    description: Optional[str] = None
    accessDelegates: Optional[List[AccessDelegate]] = None
