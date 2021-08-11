from enum import Enum


class NodeStatus(Enum):
    """Indicates the status of a node."""
    ALIVE = "ALIVE"
    """The node is alive."""
    LATE = "LATE"
    """The node's heartbeat is late."""
    LOST = "LOST"
    """The node's heartbeat has not been received for long enough that it is considered lost."""
    UNREGISTERED = "UNREGISTERED"
    """The node has unregistered from the worker pool."""
    TERMINATED = "TERMINATED"
    """The node has been terminated."""

    def is_active(self) -> bool:
        return self in (self.ALIVE, self.LATE)

    def is_gone(self) -> bool:
        return self in (self.UNREGISTERED, self.TERMINATED)

    def __str__(self) -> str:
        return self.name
