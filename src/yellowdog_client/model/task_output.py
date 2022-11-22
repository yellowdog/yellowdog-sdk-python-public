from dataclasses import dataclass
from typing import Optional

from .task_output_source import TaskOutputSource


@dataclass
class TaskOutput:
    """Defines task outputs to be uploaded following worker execution of the"""
    source: TaskOutputSource
    """The source context where the outputs can be found."""
    directoryName: Optional[str] = None
    """The pre-configured directory name; only if the source is set to TaskOutputSource.OTHER_DIRECTORY."""
    filePattern: Optional[str] = None
    """An ant-style pattern to select output files by path."""
    alwaysUpload: bool = False
    """Indicates that the outputs should still be uploaded even if the task execution failed or was aborted."""
    required: bool = False
    """Indicates that at least one output should be found otherwise the task execution is failed."""

    # KEEP
    @staticmethod
    def from_worker_directory(file_pattern: str, required: bool = False) -> 'TaskOutput':
        """Specifies that matching files from the working directory of the worker that executed the task should be uploaded."""
        return TaskOutput(
            source=TaskOutputSource.WORKER_DIRECTORY,
            filePattern=file_pattern,
            required=required
        )

    @staticmethod
    def from_directory(directory_name: str, file_pattern: str, required: bool = False) -> 'TaskOutput':
        """Specifies that matching files from the directory (defined in the agent configuration with the specified name) should be uploaded."""
        return TaskOutput(
            source=TaskOutputSource.OTHER_DIRECTORY,
            directoryName=directory_name,
            filePattern=file_pattern,
            required=required
        )

    @staticmethod
    def from_task_process() -> 'TaskOutput':
        """Specifies that the text file containing the output from the task execution process should be uploaded."""
        return TaskOutput(
            source=TaskOutputSource.PROCESS_OUTPUT,
            alwaysUpload=True
        )