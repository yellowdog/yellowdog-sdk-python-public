from enum import Enum


class NodeStatus(Enum):
    """Indicates the status of a node."""
    ALIVE = "ALIVE", True, False
    """The node is alive."""
    LATE = "LATE", True, False
    """The node's heartbeat is late."""
    LOST = "LOST", False, False
    """The node's heartbeat has not been received for long enough that it is considered lost."""
    UNREGISTERED = "UNREGISTERED", False, True
    """The node has unregistered from the worker pool."""
    TERMINATED = "TERMINATED", False, True
    """The node has been terminated."""

    def __new__(cls, value, active: bool, gone: bool):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.active = active
        obj.gone = gone
        return obj

    def __str__(self) -> str:
        return self.name
