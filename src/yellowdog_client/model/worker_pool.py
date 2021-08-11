from dataclasses import dataclass, field

from .identified import Identified
from .named import Named


@dataclass
class WorkerPool(Identified, Named):
    """A pool of workers that are managed together."""
    type: str = field(default=None, init=False)
