from abc import ABC
from typing import List, Optional

from .node_id_filter import NodeIdFilter



class NodeAction(ABC):
    action: str
    nodeIdFilter: Optional[NodeIdFilter]
    nodeTypes: Optional[List[str]]
