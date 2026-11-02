from enum import Enum


class NodeEvent(Enum):
    STARTUP_NODES_ADDED = "STARTUP_NODES_ADDED"
    """The initial provision of worker pool nodes has completed and nodes have registered (and been identified if node types are configured)"""
    NODES_ADDED = "NODES_ADDED"
    """Nodes have registered (and been identified if node types are configured) after the :attr:`STARTUP_NODES_ADDED` event has been raised."""
    NODES_REMOVED = "NODES_REMOVED"
    """Nodes have been removed (shut down, deregistered, terminated or lost) after the :attr:`STARTUP_NODES_ADDED` event has been raised."""

    def __str__(self) -> str:
        return self.name
