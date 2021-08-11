from dataclasses import dataclass
from typing import List, Optional

from .node_slot_numbering import NodeSlotNumbering


@dataclass
class NodeType:
    name: str
    count: Optional[int] = None
    min: Optional[int] = None
    sourceNames: Optional[List[str]] = None
    slotNumbering: Optional[NodeSlotNumbering] = None
