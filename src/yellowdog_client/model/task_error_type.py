from dataclasses import dataclass
from typing import ClassVar


@dataclass
class TaskErrorType:
    ALLOCATION_LOST: ClassVar[str] = "ALLOCATION_LOST"
    RESOURCE_REQUEST_FAILED: ClassVar[str] = "RESOURCE_REQUEST_FAILED"
    TIMED_OUT: ClassVar[str] = "TIMED_OUT"
    UNABLE_START_PROCESS: ClassVar[str] = "UNABLE_START_PROCESS"
    PROCESS_NON_ZERO_EXIT: ClassVar[str] = "PROCESS_NON_ZERO_EXIT"
    """The :class:`Task` was :attr:`TaskStatus.EXECUTING`, and errored with a non-zero exit code"""
    DATA_CLIENT_DISABLED: ClassVar[str] = "DATA_CLIENT_DISABLED"
    """
    The :class:`Task` could not use the data client because it was disabled during :attr:`TaskStatus.DOWNLOADING` or
    :attr:`TaskStatus.UPLOADING`.
    """

    UNKNOWN_ERROR: ClassVar[str] = "UNKNOWN_ERROR"
    OUTPUT_NOT_FOUND: ClassVar[str] = "OUTPUT_NOT_FOUND"
    INPUT_NOT_FOUND: ClassVar[str] = "INPUT_NOT_FOUND"
    TRANSITION_REFUSED: ClassVar[str] = "TRANSITION_REFUSED"
    UNABLE_WRITE_TASK_DATA: ClassVar[str] = "UNABLE_WRITE_TASK_DATA"
