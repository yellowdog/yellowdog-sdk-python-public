from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Optional

from .node_action_queue_status import NodeActionQueueStatus
from .node_status import NodeStatus


@dataclass
class NodeSummary:
    """A summary of a group of nodes."""
    statusCounts: Optional[Dict[NodeStatus, int]] = None
    """The number of nodes in each status."""
    actionQueueStatuses: Optional[Dict[NodeActionQueueStatus, int]] = None
    """The number of nodes with each action queue status."""
    lastUpdatedTime: Optional[datetime] = None
    """The last time this summary was updated."""
