from dataclasses import dataclass
from typing import List, Optional

from .keyring_accessor import KeyringAccessor
from .keyring_credential import KeyringCredential
from .named import Named


@dataclass
class Keyring(Named):
    id: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    credentials: Optional[List[KeyringCredential]] = None
    accessors: Optional[List[KeyringAccessor]] = None
