from dataclasses import dataclass, field

from .identified import Identified
from .named import Named


@dataclass
class ComputeSource(Identified, Named):
    """
    The interface implemented by all compute source model objects.

    A compute source describes a specific source for acquiring computer machine instances in order to meet the compute requirement.
    """

    type: str = field(default=None, init=False)
