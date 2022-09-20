from dataclasses import dataclass
from typing import Optional

from .cloud_provider import CloudProvider
from .operating_system_licence import OperatingSystemLicence
from .price import Price
from .usage_type import UsageType


@dataclass
class InstanceTypePrice:
    provider: Optional[CloudProvider] = None
    region: Optional[str] = None
    subRegion: Optional[str] = None
    instanceType: Optional[str] = None
    usageType: Optional[UsageType] = None
    operatingSystemLicence: Optional[OperatingSystemLicence] = None
    price: Optional[Price] = None
