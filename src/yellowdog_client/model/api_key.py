from dataclasses import dataclass
from typing import Optional


@dataclass
class ApiKey:
    id: Optional[str] = None
    secret: Optional[str] = None
