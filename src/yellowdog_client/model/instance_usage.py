from dataclasses import dataclass
from datetime import timedelta
from typing import Dict, Optional

from .cloud_provider import CloudProvider
from .instance_status import InstanceStatus


@dataclass
class InstanceUsage:
    provider: Optional[CloudProvider] = None
    region: Optional[str] = None
    instanceType: Optional[str] = None
    sourceName: Optional[str] = None
    instanceCount: int = 0
    statusDurations: Optional[Dict[InstanceStatus, timedelta]] = None
