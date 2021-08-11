from dataclasses import dataclass
from typing import Optional


@dataclass
class UpdateKeyringRequest:
    description: Optional[str] = None
