from dataclasses import dataclass
from typing import Optional

from .node_worker_target_type import NodeWorkerTargetType


@dataclass
class NodeWorkerTarget:
    targetType: NodeWorkerTargetType
    targetCount: Optional[float] = None
    customTargetCommand: Optional[str] = None

    # KEEP
    @staticmethod
    def per_node(target_count: int) -> 'NodeWorkerTarget':
        return NodeWorkerTarget(NodeWorkerTargetType.PER_NODE, target_count)

    @staticmethod
    def per_vcpus(target_count: float) -> 'NodeWorkerTarget':
        return NodeWorkerTarget(NodeWorkerTargetType.PER_VCPU, target_count)

    @staticmethod
    def per_custom_command(custom_command: str) -> 'NodeWorkerTarget':
        return NodeWorkerTarget(NodeWorkerTargetType.CUSTOM, None, custom_command)