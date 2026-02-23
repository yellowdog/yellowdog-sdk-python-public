from abc import ABC
from typing import List, Optional

from .access_delegate import AccessDelegate
from .identified import Identified
from .named import Named



class User(Identified, Named, ABC):
    """Represents a user within the YellowDog Platform."""
    type: str
    id: Optional[str]
    name: str
    email: Optional[str]
    eulaAccepted: bool
    accessDelegates: Optional[List[AccessDelegate]]
    passwordSet: bool
