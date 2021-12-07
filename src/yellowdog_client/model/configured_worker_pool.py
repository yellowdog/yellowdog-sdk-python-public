from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from .configured_worker_pool_properties import ConfiguredWorkerPoolProperties
from .node_summary import NodeSummary
from .worker_pool import WorkerPool
from .worker_pool_status import WorkerPoolStatus
from .worker_summary import WorkerSummary


@dataclass
class ConfiguredWorkerPool(WorkerPool):
    type: str = field(default="co.yellowdog.platform.model.ConfiguredWorkerPool", init=False)
    id: Optional[str] = None
    name: Optional[str] = None
    createdTime: Optional[datetime] = None
    status: Optional[WorkerPoolStatus] = None
    statusChangedTime: Optional[datetime] = None
    expectedNodeCount: int = 0
    awaitingNodes: bool = False
    workerSummary: Optional[WorkerSummary] = None
    nodeSummary: Optional[NodeSummary] = None
    properties: Optional[ConfiguredWorkerPoolProperties] = None
