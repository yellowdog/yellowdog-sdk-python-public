from enum import Enum


class TaskInputSource(Enum):
    """Defines the source contexts where task inputs can be found."""
    TASK_NAMESPACE = "TASK_NAMESPACE"
    """Task inputs from the same namespace as the task."""
    OTHER_NAMESPACE = "OTHER_NAMESPACE"
    """Task inputs from any namespace defined by the owner of the work requirement containing the task."""

    def __str__(self) -> str:
        return self.name
