from dataclasses import dataclass
from typing import Dict, List, Optional

from .node_action_group import NodeActionGroup
from .node_event import NodeEvent
from .node_type import NodeType


@dataclass
class WorkerPoolNodeConfiguration:
    nodeTypes: Optional[List[NodeType]] = None
    nodeEvents: Optional[Dict[NodeEvent, List[NodeActionGroup]]] = None
