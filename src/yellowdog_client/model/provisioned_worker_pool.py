from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from .node_summary import NodeSummary
from .provisioned_worker_pool_properties import ProvisionedWorkerPoolProperties
from .worker_pool import WorkerPool
from .worker_pool_status import WorkerPoolStatus
from .worker_summary import WorkerSummary


@dataclass
class ProvisionedWorkerPool(WorkerPool):
    type: str = field(default="co.yellowdog.platform.model.ProvisionedWorkerPool", init=False)
    id: Optional[str] = None
    name: Optional[str] = None
    createdTime: Optional[datetime] = None
    status: Optional[WorkerPoolStatus] = None
    statusChangedTime: Optional[datetime] = None
    expectedNodeCount: int = 0
    awaitingNodes: bool = False
    workerSummary: Optional[WorkerSummary] = None
    nodeSummary: Optional[NodeSummary] = None
    properties: Optional[ProvisionedWorkerPoolProperties] = None
    computeRequirementId: Optional[str] = None
    """The ID of the compute requirement used to provision the compute resource."""
