from dataclasses import dataclass
from typing import List, Optional

from .feature import Feature


@dataclass
class ApplicationDetails:
    accountId: Optional[str] = None
    accountName: Optional[str] = None
    id: Optional[str] = None
    name: Optional[str] = None
    allNamespacesReadable: bool = False
    readableNamespaces: Optional[List[str]] = None
    features: Optional[List[Feature]] = None
