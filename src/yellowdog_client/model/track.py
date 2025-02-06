from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Optional

from .identified import Identified


@dataclass
class Track(Identified):
    id: Optional[str] = None
    createdTime: Optional[datetime] = None
    tags: Optional[Dict[str, str]] = None
