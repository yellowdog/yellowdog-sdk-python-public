from dataclasses import dataclass
from typing import List, Optional


@dataclass
class NamespaceObjectsResponse:
    namespace: Optional[str] = None
    objects: Optional[List[str]] = None
