from dataclasses import dataclass
from typing import Optional


@dataclass
class UpdateApplicationRequest:
    name: Optional[str] = None
    description: Optional[str] = None
