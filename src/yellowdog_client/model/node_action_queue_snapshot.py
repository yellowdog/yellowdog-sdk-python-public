from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from .node_action import NodeAction
from .node_action_queue_status import NodeActionQueueStatus


@dataclass
class NodeActionQueueSnapshot:
    timestamp: Optional[datetime] = None
    status: Optional[NodeActionQueueStatus] = None
    waiting: Optional[List[NodeAction]] = None
    executing: Optional[List[NodeAction]] = None
    failed: Optional[NodeAction] = None
