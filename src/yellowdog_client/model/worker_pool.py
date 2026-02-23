from abc import ABC
from datetime import datetime
from typing import Optional

from .identified import Identified
from .named import Named
from .node_summary import NodeSummary
from .worker_pool_properties import WorkerPoolProperties
from .worker_pool_status import WorkerPoolStatus
from .worker_summary import WorkerSummary



class WorkerPool(Identified, Named, ABC):
    """A pool of workers that are managed together."""
    type: str
    id: Optional[str]
    name: Optional[str]
    """The name used to uniquely identify this worker pool."""
    namespace: Optional[str]
    """The namespace that this worker pool is constrained to."""
    createdTime: Optional[datetime]
    """The date and time when the worker pool was created."""
    status: Optional[WorkerPoolStatus]
    """The worker pool status."""
    statusChangedTime: Optional[datetime]
    """The date and time when the status last changed."""
    expectedNodeCount: Optional[int]
    """The expected number of nodes."""
    workerSummary: Optional[WorkerSummary]
    """The summary of the workers in this worker pool."""
    nodeSummary: Optional[NodeSummary]
    """The summary of the nodes in this worker pool."""
    properties: Optional[WorkerPoolProperties]
    """The properties of this worker pool."""
