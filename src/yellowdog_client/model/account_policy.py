from dataclasses import dataclass
from typing import Dict, Optional, Set


@dataclass
class AccountPolicy:
    instanceTagSpecification: Optional[Dict[str, Set[str]]] = None
