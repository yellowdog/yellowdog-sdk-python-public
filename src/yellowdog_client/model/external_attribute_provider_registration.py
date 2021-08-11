from dataclasses import dataclass
from typing import List, Optional

from .external_attribute_definition import ExternalAttributeDefinition


@dataclass
class ExternalAttributeProviderRegistration:
    providerName: Optional[str] = None
    maxSourcesPerRequest: int = 0
    attributes: Optional[List[ExternalAttributeDefinition]] = None
