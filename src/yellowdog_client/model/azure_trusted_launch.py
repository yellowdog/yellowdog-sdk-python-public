from dataclasses import dataclass
from typing import Optional


@dataclass
class AzureTrustedLaunch:
    enabled: bool
    secureBootEnabled: Optional[bool] = None
    vTpmEnabled: Optional[bool] = None
