from dataclasses import dataclass
from typing import List, Optional

from .feature import Feature


@dataclass
class UserPortalContext:
    userType: Optional[str] = None
    accountId: Optional[str] = None
    accountName: Optional[str] = None
    id: Optional[str] = None
    name: Optional[str] = None
    email: Optional[str] = None
    eulaAccepted: bool = False
    passwordSet: bool = False
    features: Optional[List[Feature]] = None
