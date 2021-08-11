from enum import Enum


class NodeWorkerTargetType(Enum):
    PER_NODE = "PER_NODE"
    PER_VCPU = "PER_VCPU"

    def __str__(self) -> str:
        return self.name
