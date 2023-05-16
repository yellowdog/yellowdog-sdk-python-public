from dataclasses import dataclass
from typing import List, Optional

from .cloud_provider import CloudProvider
from .instance_status import InstanceStatus
from .sort_direction import SortDirection


@dataclass
class InstanceSearch:
    sortField: Optional[str] = None
    sortDirection: Optional[SortDirection] = None
    computeRequirementId: Optional[str] = None
    computeSourceId: Optional[str] = None
    providers: Optional[List[CloudProvider]] = None
    regions: Optional[List[str]] = None
    statuses: Optional[List[InstanceStatus]] = None
    imageIds: Optional[List[str]] = None
    publicIpAddress: Optional[str] = None
    privateIpAddress: Optional[str] = None
    hostname: Optional[str] = None
