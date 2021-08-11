from dataclasses import dataclass
from typing import List

from .node_action import NodeAction


@dataclass
class NodeActionGroup:
    actions: List[NodeAction]
