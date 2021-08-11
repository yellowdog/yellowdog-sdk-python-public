from dataclasses import dataclass, field
from typing import List, Optional

from .access_delegate import AccessDelegate
from .identified import Identified
from .named import Named


@dataclass
class User(Identified, Named):
    """Represents a user within the YellowDog Platform."""
    id: Optional[str] = field(default=None, init=False)
    username: str
    name: str
    email: Optional[str] = None
    eulaAccepted: bool = False
    accessDelegates: Optional[List[AccessDelegate]] = None
