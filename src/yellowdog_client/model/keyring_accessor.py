from dataclasses import dataclass
from typing import Optional


@dataclass
class KeyringAccessor:
    accessorId: Optional[str] = None
    accessorType: Optional[str] = None
    accessorName: Optional[str] = None
