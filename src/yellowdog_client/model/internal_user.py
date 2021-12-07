from dataclasses import dataclass, field
from typing import List, Optional

from .access_delegate import AccessDelegate
from .password_state import PasswordState
from .user import User


@dataclass
class InternalUser(User):
    """Represents an internal user within the YellowDog Platform."""
    type: str = field(default="co.yellowdog.platform.model.InternalUser", init=False)
    id: Optional[str] = field(default=None, init=False)
    passwordState: Optional[PasswordState] = field(default=None, init=False)
    username: str
    name: str
    email: Optional[str] = None
    eulaAccepted: bool = False
    accessDelegates: Optional[List[AccessDelegate]] = None
