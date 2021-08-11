from dataclasses import dataclass, field
from typing import List, Optional

from .node_action import NodeAction
from .node_id_filter import NodeIdFilter
from .node_worker_target import NodeWorkerTarget


@dataclass
class NodeCreateWorkersAction(NodeAction):
    action: str = field(default="CREATE_WORKERS", init=False)
    nodeWorkers: Optional[NodeWorkerTarget] = None
    totalWorkers: Optional[int] = None
    nodeIdFilter: Optional[NodeIdFilter] = None
    nodeTypes: Optional[List[str]] = None
