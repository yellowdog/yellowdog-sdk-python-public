from dataclasses import dataclass
from typing import Optional

from .user import User


@dataclass
class AddUserResponse:
    user: Optional[User] = None
