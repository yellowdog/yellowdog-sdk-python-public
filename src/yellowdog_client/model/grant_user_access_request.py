from dataclasses import dataclass
from typing import Optional


@dataclass
class GrantUserAccessRequest:
    userId: Optional[str] = None
    userPassword: Optional[str] = None
