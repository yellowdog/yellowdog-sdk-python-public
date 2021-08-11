from dataclasses import dataclass
from typing import Optional


@dataclass
class ObjectPath:
    name: str
    displayName: Optional[str] = None
    prefix: bool = False
