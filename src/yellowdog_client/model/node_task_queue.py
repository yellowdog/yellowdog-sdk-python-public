from dataclasses import dataclass


@dataclass
class NodeTaskQueue:
    """Describes the current state of a node's local task queue for a specific task group."""
    workerUtilisation: float = 0
    """
    A value between 0 and 1 showing the current utilisation as a
    percentage of time available spent working for the workers
    claimed for the task group on this node.
    """

