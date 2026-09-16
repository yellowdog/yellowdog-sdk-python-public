from enum import Enum


class ClusterOperationType(Enum):
    PROVISION_CLUSTER = "PROVISION_CLUSTER"
    TERMINATE_CLUSTER = "TERMINATE_CLUSTER"

    def __str__(self) -> str:
        return self.name
