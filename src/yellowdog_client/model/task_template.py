from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class TaskTemplate:
    taskType: Optional[str] = None
    taskData: Optional[str] = None
    environment: Optional[Dict[str, str]] = None
