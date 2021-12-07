from dataclasses import dataclass, field

from .identified import Identified


@dataclass
class Allowance(Identified):
    type: str = field(default=None, init=False)
