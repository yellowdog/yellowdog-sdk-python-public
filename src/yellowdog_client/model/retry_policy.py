from dataclasses import dataclass
from typing import Optional

from .selection import Selection
from .task_error_selector import TaskErrorSelector


@dataclass
class RetryPolicy:
    """
    Policy that can be specified in a :class:`RunSpecification` to control how many times a :class:`Task` can retry in the
    event that an attempt to execute the :class:`Task` errors.
    """

    maxRetries: int = 0
    """
    The maximum number of times a :class:`Task` can be retried. The maximum total number of attempts will always be
    `maxRetries + 1` because the first attempt is not a retry. Must be 0 or higher. Zero is allowed if you want to be
    explicit, and to make it easy to change the number of retries without having to omit the policy. Specifying zero
    is effectively the same as having no :class:`RetryPolicy`.
    """

    retryErrors: Optional[Selection[TaskErrorSelector]] = None
    """
    Optional :class:`Selection` which, if specified, only allows attempts matching the :class:`Selection` to be retried.
    Note that it is only the :class:`TaskError` from the most recent attempt that is evaluated by the :class:`Selection`.
    """


# KEEP
def retry(*, max: int, when: Optional[Selection[TaskErrorSelector]] = None) -> RetryPolicy:
    """
    Creates a :class:`RetryPolicy` that will retry tasks that would otherwise be failed. The :class:`RetryPolicy`
    is always evaluated before the :class:`FailurePolicy`.`

    **Retry all tasks**
    Allows a maximum of one retry i.e. a maximum of two attempts, the original attempt plus one retry.
    .. code-block:: python
        retry(max=1)

    **Retry depending on last error**
    The :class:`TaskErrorSelector` allows targeting of specific errors. Combined with :class:`Selection` to include and
    exclude specific tasks.
    In this example, `oom` is a more specific variant of `non_zero_exit_code`.
    If no destination matches, the task will enter the failed state as normal.
    .. code-block:: python
        oom = TaskErrorSelector(processExitCodes=includes([ 137 ]))
        preempted = TaskErrorSelector(errorTypes=includes([ TaskErrorType.ALLOCATION_LOST ]))
        retry(max=1, when=includes([oom, preempted]))

    **Retry using excludes**
    If you want to always retry except in specific cases, you may want to use excludes instead.
    .. code-block:: python
        exceptional_errors = TaskErrorSelector(errorTypes=includes([ TaskErrorType.TIMED_OUT, TaskErrorType.DATA_CLIENT_DISABLED, TaskErrorType.UNKNOWN_ERROR ]))
        retry(max=1, when=excludes([exceptional_errors]))

    **Retry using includes and excludes**
    Sometimes using includes is not enough, and you will need touse excludes as well. To retry all non-zero exit codes
    unless it was an out of memory error, you must include all non-zero exit codes, explicitly excluding 137 (the exit
    code typically used denote out of memory).
    .. code-block:: python
        oom = TaskErrorSelector(processExitCodes=includes([ 137 ]))
        non_zero_exit_code = TaskErrorSelector(errorTypes=includes([ TaskErrorType.PROCESS_NON_ZERO_EXIT ]))
        retry(max=1, when=Selection(includes=[non_zero_exit_code], excludes=[oom]))

        # OR:
        non_zero_exit_code_except_oom = TaskErrorSelector(errorTypes=includes([ TaskErrorType.PROCESS_NON_ZERO_EXIT ]), processExitCodes=includes([ 137 ]))
        retry(max=1, when=includes([non_zero_exit_code_except_oom]))
    """
    return RetryPolicy(maxRetries=max, retryErrors=when)