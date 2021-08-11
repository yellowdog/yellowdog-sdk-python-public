from dataclasses import dataclass
from typing import List, Optional

from .external_attribute_provider_query_source import ExternalAttributeProviderQuerySource


@dataclass
class ExternalAttributeProviderQuery:
    attributes: Optional[List[str]] = None
    sources: Optional[List[ExternalAttributeProviderQuerySource]] = None
