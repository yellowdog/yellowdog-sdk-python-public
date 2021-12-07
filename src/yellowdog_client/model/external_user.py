from dataclasses import dataclass, field
from typing import List, Optional

from .access_delegate import AccessDelegate
from .authentication_provider import AuthenticationProvider
from .password_state import PasswordState
from .user import User


@dataclass
class ExternalUser(User):
    """Represents an external user within the YellowDog Platform."""
    type: str = field(default="co.yellowdog.platform.model.ExternalUser", init=False)
    externalId: str = field(default=None, init=False)
    authenticationProvider: AuthenticationProvider = field(default=None, init=False)
    id: Optional[str] = field(default=None, init=False)
    passwordState: Optional[PasswordState] = field(default=None, init=False)
    name: str
    email: Optional[str] = None
    eulaAccepted: bool = False
    accessDelegates: Optional[List[AccessDelegate]] = None
