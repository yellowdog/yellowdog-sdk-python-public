from dataclasses import dataclass
from typing import Optional

from .keyring import Keyring


@dataclass
class CreateKeyringResponse:
    keyring: Optional[Keyring] = None
    keyringPassword: Optional[str] = None
