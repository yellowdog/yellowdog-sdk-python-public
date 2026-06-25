from dataclasses import dataclass
from typing import Optional

from .selection import Selection
from .task_status import TaskStatus


@dataclass
class TaskErrorSelector:
    """
    Selector for :class:`TaskError` that 'ANDs' the containing :class:`Selection`\\s. At least one :class:`Selection` must be
    specified.
    """

    errorTypes: Optional[Selection[str]] = None
    """@see TaskErrorType"""
    statusesAtFailure: Optional[Selection[TaskStatus]] = None
    """
    """

    processExitCodes: Optional[Selection[int]] = None
    """
    A :class:`Selection` of the process exit codes the :class:`Task` must have errored for, can be null.

    Note that if there is a processExitCode, the error type must be :attr:`TaskErrorType.PROCESS_NON_ZERO_EXIT`.
    """

