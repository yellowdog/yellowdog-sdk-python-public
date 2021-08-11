from dataclasses import dataclass
from typing import List, Optional

from .cloud_provider import CloudProvider
from .double_range import DoubleRange
from .instant_range import InstantRange
from .long_range import LongRange
from .node_status import NodeStatus
from .sort_direction import SortDirection
from .worker_status import WorkerStatus


@dataclass
class NodeSearch:
    workerPoolId: Optional[str] = None
    statuses: Optional[List[NodeStatus]] = None
    providers: Optional[List[CloudProvider]] = None
    instanceId: Optional[str] = None
    region: Optional[str] = None
    instanceType: Optional[str] = None
    ram: Optional[DoubleRange] = None
    vcpus: Optional[DoubleRange] = None
    workerClaimCount: Optional[LongRange] = None
    workerRegisteredTime: Optional[InstantRange] = None
    workerTaskGroupId: Optional[str] = None
    workerTag: Optional[str] = None
    workerStatuses: Optional[List[WorkerStatus]] = None
    sortField: Optional[str] = None
    sortDirection: Optional[SortDirection] = None
