from dataclasses import dataclass
from typing import Optional


@dataclass
class ObjectPathsRequest:
    namespace: Optional[str] = None
    flat: bool = False
    prefix: Optional[str] = None
