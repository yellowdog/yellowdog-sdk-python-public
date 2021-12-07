from dataclasses import dataclass
from typing import Optional

from .task_input_source import TaskInputSource


@dataclass
class TaskInput:
    """Defines task inputs to be downloaded prior to worker execution of the task."""
    source: TaskInputSource
    """The source context where the inputs can be found."""
    objectNamePattern: str
    """An ant-style pattern to select objects by name."""
    namespace: Optional[str] = None
    """The namespace containing matching objects; only if the source is set to TaskInputSource.OTHER_NAMESPACE."""
    required: bool = False
    """Indicates that at least one input should be found otherwise the task execution is failed."""

    # KEEP
    @staticmethod
    def from_task_namespace(object_name_pattern: str, required: bool = False) -> 'TaskInput':
        """Specifies that matching objects from the same namespace as the task should be downloaded to the working directory prior to task execution."""
        return TaskInput(
            source=TaskInputSource.TASK_NAMESPACE,
            objectNamePattern=object_name_pattern,
            required=required
        )

    @staticmethod
    def from_namespace(namespace: str, object_name_pattern: str, required: bool = False) -> 'TaskInput':
        """Specifies that matching objects from the supplied namespace should be downloaded to the working directory prior to task execution."""
        return TaskInput(
            source=TaskInputSource.OTHER_NAMESPACE,
            namespace=namespace,
            objectNamePattern=object_name_pattern,
            required=required
        )