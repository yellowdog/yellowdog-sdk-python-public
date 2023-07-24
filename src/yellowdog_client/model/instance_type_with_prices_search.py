from dataclasses import dataclass
from typing import Optional

from .cloud_provider import CloudProvider
from .operating_system_licence import OperatingSystemLicence
from .sort_direction import SortDirection


@dataclass
class InstanceTypeWithPricesSearch:
    provider: CloudProvider
    operatingSystemLicence: OperatingSystemLicence
    sortField: Optional[str] = None
    sortDirection: Optional[SortDirection] = None
    instanceTypeName: Optional[str] = None
    region: Optional[str] = None
    subRegion: Optional[str] = None
