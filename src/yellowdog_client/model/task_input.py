from dataclasses import dataclass, field
from typing import Optional

from .task_input_source import TaskInputSource
from .task_input_verification import TaskInputVerification
from .task_input_verification_status import TaskInputVerificationStatus


@dataclass
class TaskInput:
    """Defines task inputs to be downloaded prior to worker execution of the task."""
    verificationStatus: Optional[TaskInputVerificationStatus] = field(default=None, init=False)
    """The task input verification status."""
    source: TaskInputSource
    """The source context where the inputs can be found."""
    objectNamePattern: str
    """An ant-style pattern to select objects by name."""
    namespace: Optional[str] = None
    """The namespace containing matching objects; only if the source is set to TaskInputSource.OTHER_NAMESPACE."""
    verification: Optional[TaskInputVerification] = None
    """Indicates if and how the Scheduler should verify the existence of a task input prior to starting the task."""

    # KEEP
    @staticmethod
    def from_task_namespace(object_name_pattern: str, verification: TaskInputVerification = None) -> 'TaskInput':
        """Specifies that matching objects from the same namespace as the task should be downloaded to the working directory prior to task execution."""
        return TaskInput(
            source=TaskInputSource.TASK_NAMESPACE,
            objectNamePattern=object_name_pattern,
            verification=verification
        )

    @staticmethod
    def from_namespace(namespace: str, object_name_pattern: str, verification: TaskInputVerification = None) -> 'TaskInput':
        """Specifies that matching objects from the supplied namespace should be downloaded to the working directory prior to task execution."""
        return TaskInput(
            source=TaskInputSource.OTHER_NAMESPACE,
            namespace=namespace,
            objectNamePattern=object_name_pattern,
            verification=verification
        )