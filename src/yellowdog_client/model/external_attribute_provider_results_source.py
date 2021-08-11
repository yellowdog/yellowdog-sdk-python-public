from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class ExternalAttributeProviderResultsSource:
    id: str
    attributes: Optional[Dict[str, Any]] = None
