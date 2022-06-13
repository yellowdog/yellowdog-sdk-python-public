from dataclasses import dataclass
from typing import Optional


@dataclass
class AddUserRequest:
    username: str
    name: str
    email: Optional[str] = None
