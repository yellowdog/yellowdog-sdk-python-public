from enum import Enum


class NodeActionQueueStatus(Enum):
    """The status of the action queue for a specific node."""
    EMPTY = "EMPTY"
    """No actions are waiting for the node to execute."""
    WAITING = "WAITING"
    """Actions are waiting for the node to retrieve and execute."""
    EXECUTING = "EXECUTING"
    """Actions are currently being executed by the node."""
    FAILED = "FAILED"
    """The node has failed to execute an action and the queue is stopped."""

    def __str__(self) -> str:
        return self.name
