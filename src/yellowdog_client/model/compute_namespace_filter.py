from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from .filter import Filter


@dataclass
class ComputeNamespaceFilter(Filter):
    fromTime: datetime
    untilTime: datetime
    createdById: Optional[str] = None
    namespaces: Optional[List[str]] = None
