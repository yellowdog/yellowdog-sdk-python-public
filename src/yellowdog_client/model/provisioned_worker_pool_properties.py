from dataclasses import dataclass
from datetime import timedelta
from typing import Optional

from .auto_shutdown import AutoShutdown
from .node_worker_target import NodeWorkerTarget
from .worker_pool_node_configuration import WorkerPoolNodeConfiguration
from .worker_pool_properties import WorkerPoolProperties


@dataclass
class ProvisionedWorkerPoolProperties(WorkerPoolProperties):
    """Defines properties to determine the behaviour that the Scheduler service should use when managing a provisioned worker pool."""
    createNodeWorkers: Optional[NodeWorkerTarget] = None
    """How many workers to create on each node."""
    minNodes: Optional[int] = None
    """The minimum number of nodes that the worker pool can be scaled down to."""
    maxNodes: Optional[int] = None
    """The maximum number of nodes that the worker pool can be scaled up to."""
    nodeBootTimeout: Optional[timedelta] = None
    """The time given for a node to be registered before it is considered to have failed."""
    idleNodeShutdown: Optional[AutoShutdown] = None
    """Determines the auto shutdown behaviour applied for idle nodes."""
    idlePoolShutdown: Optional[AutoShutdown] = None
    """Determines the auto shutdown behaviour applied for an idle pool."""
    workerTag: Optional[str] = None
    """An optional tag value that will be attached to all workers in this pool and used to constrain worker allocation."""
    nodeConfiguration: Optional[WorkerPoolNodeConfiguration] = None
