from dataclasses import dataclass
from typing import List, Optional

from .cloud_provider import CloudProvider
from .operating_system_licence import OperatingSystemLicence
from .sort_direction import SortDirection
from .usage_type import UsageType


@dataclass
class InstanceTypePriceSearch:
    providers: Optional[List[CloudProvider]] = None
    region: Optional[str] = None
    subRegion: Optional[str] = None
    instanceType: Optional[str] = None
    usageTypes: Optional[List[UsageType]] = None
    operatingSystemLicences: Optional[List[OperatingSystemLicence]] = None
    sortField: Optional[str] = None
    sortDirection: Optional[SortDirection] = None
