from dataclasses import dataclass

from .node_worker_target_type import NodeWorkerTargetType


@dataclass
class NodeWorkerTarget:
    targetCount: float
    targetType: NodeWorkerTargetType
