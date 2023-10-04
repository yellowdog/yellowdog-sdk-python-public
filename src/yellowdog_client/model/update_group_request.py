from dataclasses import dataclass
from typing import Optional


@dataclass
class UpdateGroupRequest:
    name: str
    description: Optional[str] = None
