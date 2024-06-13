from dataclasses import dataclass, field
from typing import List, Optional

from .feature import Feature
from .identified import Identified
from .named import Named


@dataclass
class Account(Identified, Named):
    """Represents a user account within the YellowDog Platform."""
    id: Optional[str] = field(default=None, init=False)
    name: str
    features: Optional[List[Feature]] = None
