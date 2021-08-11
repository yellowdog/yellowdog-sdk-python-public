from dataclasses import dataclass
from typing import List, Optional


@dataclass
class AllowanceExhaustedNotification:
    allowanceId: Optional[str] = None
    allowanceDescription: Optional[str] = None
    exhaustedSourceIds: Optional[List[str]] = None
