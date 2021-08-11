from dataclasses import dataclass
from typing import List, Optional


@dataclass
class ErrorResponse:
    errorType: str
    message: Optional[str] = None
    detail: Optional[List[str]] = None
