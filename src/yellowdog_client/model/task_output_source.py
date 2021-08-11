from enum import Enum


class TaskOutputSource(Enum):
    """Defines the source contexts where the task outputs can be found."""
    WORKER_DIRECTORY = "WORKER_DIRECTORY"
    """Task outputs from the working directory of the worker that executed the task."""
    OTHER_DIRECTORY = "OTHER_DIRECTORY"
    """Task outputs from a directory defined in the agent configuration."""
    PROCESS_OUTPUT = "PROCESS_OUTPUT"
    """The file containing the output from the process executing the task."""

    def __str__(self) -> str:
        return self.name
