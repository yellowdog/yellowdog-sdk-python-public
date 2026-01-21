from dataclasses import dataclass
from datetime import timedelta
from typing import Optional


@dataclass
class TaskWorkingTime:
    downloading: Optional[timedelta] = None
    executing: Optional[timedelta] = None
    uploading: Optional[timedelta] = None
