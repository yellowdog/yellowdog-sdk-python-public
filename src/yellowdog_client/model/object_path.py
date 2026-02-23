from dataclasses import dataclass
from typing import ClassVar, Optional


@dataclass
class ObjectPath:
    DEFAULT_DELIMITER: ClassVar[str] = "/"
    name: str
    displayName: Optional[str] = None
    prefix: bool = False
