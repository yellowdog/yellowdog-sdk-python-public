from dataclasses import dataclass, field
from typing import List, Optional

from .application import Application
from .identified import Identified
from .named import Named
from .user import User


@dataclass
class Account(Identified, Named):
    """Represents a user account within the YellowDog Platform."""
    id: Optional[str] = field(default=None, init=False)
    name: str
    users: Optional[List[User]] = None
    applications: Optional[List[Application]] = None
