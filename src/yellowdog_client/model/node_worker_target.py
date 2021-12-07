from dataclasses import dataclass

from .node_worker_target_type import NodeWorkerTargetType


@dataclass
class NodeWorkerTarget:
    targetCount: float
    targetType: NodeWorkerTargetType

    # KEEP
    @staticmethod
    def per_node(target_count: int) -> 'NodeWorkerTarget':
        return NodeWorkerTarget(target_count, NodeWorkerTargetType.PER_NODE)

    @staticmethod
    def per_vcpus(target_count: float) -> 'NodeWorkerTarget':
        return NodeWorkerTarget(target_count, NodeWorkerTargetType.PER_VCPU)