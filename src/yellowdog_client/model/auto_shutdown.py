from dataclasses import dataclass
from datetime import timedelta
from typing import Optional


@dataclass
class AutoShutdown:
    enabled: Optional[bool] = None
    timeout: Optional[timedelta] = None
