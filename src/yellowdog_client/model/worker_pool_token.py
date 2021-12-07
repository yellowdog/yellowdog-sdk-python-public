from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class WorkerPoolToken:
    """Defines a secret token shared with an agent in advance of its registration."""
    secret: Optional[str] = None
    """The token secret."""
    expiryTime: Optional[datetime] = None
    """The token expiry time."""
