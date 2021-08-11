from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from .external_attribute_provider_results_source import ExternalAttributeProviderResultsSource


@dataclass
class ExternalAttributeProviderResults:
    sources: Optional[List[ExternalAttributeProviderResultsSource]] = None
    expires: Optional[datetime] = None
