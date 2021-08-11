from dataclasses import dataclass
from typing import Optional


@dataclass
class KeyringAccessSecrets:
    keyringPassword: Optional[str] = None
    accessorSecret: Optional[str] = None
