from dataclasses import dataclass
from typing import Optional

from .identified import Identified


@dataclass
class RoleSummary(Identified):
    id: Optional[str] = None
    name: Optional[str] = None
