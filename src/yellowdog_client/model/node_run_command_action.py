from dataclasses import dataclass, field
from typing import Dict, List, Optional

from .node_action import NodeAction
from .node_id_filter import NodeIdFilter


@dataclass
class NodeRunCommandAction(NodeAction):
    action: str = field(default="RUN_COMMAND", init=False)
    path: str
    arguments: Optional[List[str]] = None
    environment: Optional[Dict[str, str]] = None
    nodeIdFilter: Optional[NodeIdFilter] = None
    nodeTypes: Optional[List[str]] = None
