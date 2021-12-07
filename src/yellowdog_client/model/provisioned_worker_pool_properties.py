from dataclasses import dataclass
from datetime import timedelta
from typing import List, Optional

from .node_worker_target import NodeWorkerTarget
from .worker_pool_node_configuration import WorkerPoolNodeConfiguration
from .worker_pool_properties import WorkerPoolProperties
from .worker_pool_shutdown_condition import WorkerPoolShutdownCondition


@dataclass
class ProvisionedWorkerPoolProperties(WorkerPoolProperties):
    """Defines properties to determine the behaviour that the Scheduler service should use when managing a provisioned worker pool."""
    createNodeWorkers: Optional[NodeWorkerTarget] = None
    """How many workers to create on each node."""
    minNodes: Optional[int] = None
    """The minimum number of nodes that the worker pool can be scaled down to."""
    maxNodes: Optional[int] = None
    """The maximum number of nodes that the worker pool can be scaled up to."""
    nodeBootTimeLimit: Optional[timedelta] = None
    """The time given for a node to be registered before it is considered to have failed."""
    nodeIdleTimeLimit: Optional[timedelta] = None
    """The time that a node can be idle with all workers unclaimed before it is terminated."""
    nodeIdleGracePeriod: Optional[timedelta] = None
    """The time after a node registers where the idle check is not applied."""
    autoShutdown: Optional[bool] = None
    """If true, the worker pool will be automatically shutdown, according to the configured autoShutdownConditions."""
    autoShutdownConditions: Optional[List[WorkerPoolShutdownCondition]] = None
    """A list of conditions that can cause the worker pool to be automatically shutdown if one or more conditions is met."""
    workerTag: Optional[str] = None
    """An optional tag value that will be attached to all workers in this pool and used to constrain worker allocation."""
    nodeConfiguration: Optional[WorkerPoolNodeConfiguration] = None
