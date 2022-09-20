from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from .identified import Identified
from .node_action_queue_status import NodeActionQueueStatus
from .node_details import NodeDetails
from .node_status import NodeStatus
from .worker import Worker


@dataclass
class Node(Identified):
    """Describes an instance within a worker pool."""
    id: Optional[str] = None
    """The ID of the node."""
    workerPoolId: Optional[str] = None
    """The ID of the worker pool containing the node."""
    details: Optional[NodeDetails] = None
    """The details of the node."""
    status: Optional[NodeStatus] = None
    """The status of this instance."""
    statusChangedTime: Optional[datetime] = None
    """The date and time when the status last changed."""
    registeredTime: Optional[datetime] = None
    """The time when the node was registered."""
    workers: Optional[List[Worker]] = None
    """The workers on this instance."""
    actionQueueStatus: Optional[NodeActionQueueStatus] = None
    """The status of the action queue for the node."""
