from dataclasses import dataclass
from typing import Optional

from .user import User


@dataclass
class AddUserResponse:
    token: Optional[str] = None
    user: Optional[User] = None
