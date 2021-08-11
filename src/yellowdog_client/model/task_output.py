from dataclasses import dataclass
from typing import Optional

from .task_output_source import TaskOutputSource


@dataclass
class TaskOutput:
    """Defines task outputs to be uploaded following worker execution of the task."""
    source: TaskOutputSource
    """The source context where the outputs can be found."""
    directoryName: Optional[str] = None
    """The pre-configured directory name; only if the source is set to TaskOutputSource.OTHER_DIRECTORY."""
    filePattern: Optional[str] = None
    """An ant-style pattern to select output files by path."""
    uploadOnFailed: bool = False
    """Indicates that the outputs should still be uploaded even if the task execution fails."""
