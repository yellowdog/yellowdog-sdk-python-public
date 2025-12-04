from dataclasses import dataclass
from typing import List, Optional

from .instant_range import InstantRange
from .log_level import LogLevel


@dataclass
class GetLogsRequest:
    limit: Optional[int] = None
    level: Optional[LogLevel] = None
    components: Optional[List[str]] = None
    entityIds: Optional[List[str]] = None
    namespaces: Optional[List[str]] = None
    text: Optional[str] = None
    range: Optional[InstantRange] = None
