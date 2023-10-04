from dataclasses import dataclass
from typing import Optional


@dataclass
class AddGroupRequest:
    name: str
    description: Optional[str] = None
