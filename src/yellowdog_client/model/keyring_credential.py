from dataclasses import dataclass
from typing import Optional

from .named import Named


@dataclass
class KeyringCredential(Named):
    name: Optional[str] = None
    description: Optional[str] = None
    type: Optional[str] = None
