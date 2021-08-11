from dataclasses import dataclass, field
from typing import Optional

from .worker_pool_node_configuration import WorkerPoolNodeConfiguration
from .worker_pool_properties import WorkerPoolProperties


@dataclass
class ConfiguredWorkerPoolProperties(WorkerPoolProperties):
    """Defines properties to determine the behaviour that the Scheduler service should use when managing a configured worker pool."""
    type: str = field(default="co.yellowdog.platform.model.ConfiguredWorkerPoolProperties", init=False)
    nodeConfiguration: Optional[WorkerPoolNodeConfiguration] = None
