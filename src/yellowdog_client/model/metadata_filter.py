from dataclasses import dataclass
from typing import Optional


@dataclass
class MetadataFilter:
    key: str
    value: Optional[str] = None
