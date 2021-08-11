from dataclasses import dataclass
from typing import Optional


@dataclass
class AddApplicationRequest:
    name: str
    description: Optional[str] = None
