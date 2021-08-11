from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class ExternalAttributeProviderQuerySource:
    id: Optional[str] = None
    source: Optional[Dict[str, Any]] = None
    image: Optional[Dict[str, Any]] = None
