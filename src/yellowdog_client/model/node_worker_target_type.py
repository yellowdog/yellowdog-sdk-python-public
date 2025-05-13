from enum import Enum


class NodeWorkerTargetType(Enum):
    PER_NODE = "PER_NODE"
    PER_VCPU = "PER_VCPU"
    CUSTOM = "CUSTOM"

    def __str__(self) -> str:
        return self.name
