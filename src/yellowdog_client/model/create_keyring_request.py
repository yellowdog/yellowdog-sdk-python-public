from dataclasses import dataclass
from typing import Optional


@dataclass
class CreateKeyringRequest:
    name: str
    description: Optional[str] = None
    creatorSecret: Optional[str] = None
