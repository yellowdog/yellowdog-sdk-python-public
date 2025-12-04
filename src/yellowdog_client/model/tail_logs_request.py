from dataclasses import dataclass
from typing import List, Optional

from .log_level import LogLevel


@dataclass
class TailLogsRequest:
    level: Optional[LogLevel] = None
    components: Optional[List[str]] = None
    entityIds: Optional[List[str]] = None
    namespaces: Optional[List[str]] = None
    text: Optional[str] = None
