from dataclasses import dataclass
from typing import List

from .resubmission_destination import ResubmissionDestination


@dataclass
class FailurePolicy:
    """
    Policy that can be specified in a :class:`RunSpecification` to control what to do before a :class:`Task` transitions to
    the :attr:`TaskStatus.FAILED` status. The :class:`FailurePolicy` is always applied after the :class:`RetryPolicy`.

    A :class:`FailurePolicy` can be used in conjunction with a :class:`RetryPolicy` or the deprecated
    :meth:`RunSpecification.set_maximum_task_retries(integer)`}/:meth:`RunSpecification.set_retryable_errors(list)`.
    """

    resubmissionDestinations: List[ResubmissionDestination]
    """
    A :class:`List` of :class:`ResubmissionDestination`\\s that are evaluated in order from most to least important. The
    first :class:`ResubmissionDestination` that matches the last :class:`TaskError` that caused the Task to error will
    be used.
    """


# KEEP
def failure(resubmit: List[ResubmissionDestination]) -> FailurePolicy:
    """
    Creates a :class:`FailurePolicy` that will resubmit tasks that would otherwise be failed, to different :class:`TaskGroup`s.
    The :class:`FailurePolicy` is always evaluated after the :class:`RetryPolicy`.`

    **Resubmit all tasks**
    .. code-block:: python
        failure(resubmit=[destination(toTaskGroup="name-of-some-other-task-group")])

    **Resubmit depending on last error**
    Destinations are always evaluated in order, so make sure to put the most specific "when" clauses first.
    In this example, `oom` is a more specific variant of `non_zero_exit_code`.
    If no destination matches, the task will enter the failed state as normal.
    .. code-block:: python
        oom = TaskErrorSelector(processExitCodes=includes([ 137 ]))
        non_zero_exit_code = TaskErrorSelector(errorTypes=includes([ TaskErrorType.PROCESS_NON_ZERO_EXIT ]))
        preempted = TaskErrorSelector(errorTypes=includes([ TaskErrorType.ALLOCATION_LOST ]))

        failure(resubmit=[
            destination(when=includes([oom]), toTaskGroup="high-mem-task-group"),
            destination(when=includes([non_zero_exit_code]), toTaskGroup="other-task-group")
            destination(when=includes([preempted]), toTaskGroup="ondemand-task-group")
        ])
    """
    return FailurePolicy(resubmissionDestinations=resubmit)