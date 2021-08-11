from dataclasses import dataclass
from typing import List, Optional

from .node_action_group import NodeActionGroup


@dataclass
class AddNodeActionsRequest:
    actionGroups: List[NodeActionGroup]
    nodeIdFilterList: Optional[List[str]] = None
