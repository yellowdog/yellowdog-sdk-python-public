from dataclasses import dataclass
from typing import List, Optional


@dataclass
class DashboardRequest:
    namespaces: Optional[List[str]] = None
