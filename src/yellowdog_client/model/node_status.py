from __future__ import annotations

from enum import Enum


class NodeStatus(Enum):
    """Indicates the status of a node."""
    active: bool
    """Returns true, if the status indicates the node is active; otherwise, false."""
    gone: bool
    """Returns true, if the status indicates the node has gone; otherwise, false."""

    RUNNING = "RUNNING", True, False
    """The node is running and its heartbeat is being received."""
    LATE = "LATE", True, False
    """The node's heartbeat is late."""
    LOST = "LOST", False, True
    """The node's heartbeat has not been received for long enough that it is considered lost."""
    DEREGISTERED = "DEREGISTERED", False, True
    """The node has been deregistered from the worker pool."""
    TERMINATED = "TERMINATED", False, True
    """The node has been terminated."""

    def __new__(cls, value: str, active: bool, gone: bool) -> NodeStatus:
        obj = object.__new__(cls)
        obj._value_ = value
        obj.active = active
        obj.gone = gone
        return obj

    def __str__(self) -> str:
        return self.name
