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
