from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from .filter import Filter


@dataclass
class ComputeNamespaceFilter(Filter):
    fromTime: datetime
    untilTime: datetime
    createdById: Optional[str] = None
