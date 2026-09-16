from enum import Enum


class ClusterStatus(Enum):
    PROVISIONING = "PROVISIONING"
    RUNNING = "RUNNING"
    TERMINATING = "TERMINATING"
    TERMINATED = "TERMINATED"

    def __str__(self) -> str:
        return self.name
