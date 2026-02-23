from abc import ABC
from typing import Optional

from .worker_pool_node_configuration import WorkerPoolNodeConfiguration



class WorkerPoolProperties(ABC):
    nodeConfiguration: Optional[WorkerPoolNodeConfiguration]
    workerTag: Optional[str]
    metricsEnabled: Optional[bool]
