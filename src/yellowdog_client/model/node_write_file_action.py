from dataclasses import dataclass, field
from typing import List, Optional

from .node_action import NodeAction
from .node_id_filter import NodeIdFilter


@dataclass
class NodeWriteFileAction(NodeAction):
    action: str = field(default="WRITE_FILE", init=False)
    path: str
    content: Optional[str] = None
    nodeIdFilter: Optional[NodeIdFilter] = None
    nodeTypes: Optional[List[str]] = None
