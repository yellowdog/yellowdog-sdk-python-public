from dataclasses import dataclass
from typing import Optional


@dataclass
class UserLoginResponse:
    id: Optional[str] = None
    name: Optional[str] = None
    accountName: Optional[str] = None
    eulaAccepted: bool = False
    jwt: Optional[str] = None
