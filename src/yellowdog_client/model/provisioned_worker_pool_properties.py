from dataclasses import dataclass, field
from datetime import timedelta
from typing import List, Optional

from .node_worker_target import NodeWorkerTarget
from .worker_pool_node_configuration import WorkerPoolNodeConfiguration
from .worker_pool_properties import WorkerPoolProperties
from .worker_pool_shutdown_condition import WorkerPoolShutdownCondition


@dataclass
class ProvisionedWorkerPoolProperties(WorkerPoolProperties):
    """Defines properties to determine the behaviour that the Scheduler service should use when managing a provisioned worker pool."""
    type: str = field(default="co.yellowdog.platform.model.ProvisionedWorkerPoolProperties", init=False)
    createNodeWorkers: Optional[NodeWorkerTarget] = None
    """How many workers to create on each node."""
    singleUse: Optional[bool] = None
    """Indicates if a node should be terminated as soon as all its workers are released back to the worker pool."""
    bootTimeLimit: Optional[timedelta] = None
    """The time given for a node to be registered before it is considered to have failed."""
    autoShutdown: Optional[bool] = None
    """If true, the worker pool will be automatically shutdown, according to the configured autoShutdownConditions."""
    autoReprovision: Optional[bool] = None
    """If true, nodes will be automatically reprovisioned if this worker pool is unable to meet the required number of worker claims."""
    autoShutdownConditions: Optional[List[WorkerPoolShutdownCondition]] = None
    """A list of conditions that can cause the worker pool to be automatically shutdown if one or more conditions is met."""
    workerTag: Optional[str] = None
    """An optional tag value that will be attached to all workers in this pool and used to constrain worker allocation."""
    nodeConfiguration: Optional[WorkerPoolNodeConfiguration] = None
