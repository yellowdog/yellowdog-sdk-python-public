from dataclasses import dataclass, field

from .identified import Identified
from .named import Named


@dataclass
class User(Identified, Named):
    """Represents a user within the YellowDog Platform."""
    type: str = field(default=None, init=False)
