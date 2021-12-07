from dataclasses import dataclass
from typing import Optional

from .worker_pool_node_configuration import WorkerPoolNodeConfiguration
from .worker_pool_properties import WorkerPoolProperties


@dataclass
class ConfiguredWorkerPoolProperties(WorkerPoolProperties):
    """Defines properties to determine the behaviour that the Scheduler service should use when managing a configured worker pool."""
    nodeConfiguration: Optional[WorkerPoolNodeConfiguration] = None
    targetNodeCount: Optional[int] = None
    """The number of nodes that will be configured to register with this worker pool."""
