from dataclasses import dataclass, field

from .identified import Identified
from .named import Named


@dataclass
class ComputeRequirementTemplate(Identified, Named):
    type: str = field(default=None, init=False)
