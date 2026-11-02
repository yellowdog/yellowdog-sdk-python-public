from dataclasses import dataclass
from typing import Optional

from .selection import Selection
from .task_error_selector import TaskErrorSelector


@dataclass
class ResubmissionDestination:
    """
    A destination to which tasks that fail can be resubmitted. A resubmitted task is set to
    :attr:`TaskStatus.RESUBMITTED` instead of :attr:`TaskStatus.FAILED`, and a copy of it is added to the destination
    :class:`TaskGroup`. If the destination :class:`TaskGroup` does not exist in the same :class:`WorkRequirement`, or is no
    longer able to accept tasks, the task is then set to :attr:`TaskStatus.FAILED`.

    @see FailurePolicy
    """

    destinationTaskGroup: str
    """Name of the :class:`TaskGroup` to which any matching tasks that fail should be resubmitted."""
    resubmitErrors: Optional[Selection[TaskErrorSelector]] = None
    """
    Optional :class:`Selection` to determine which :class:`Task`\\s are eligible to be resubmitted to the to destination
    :class:`TaskGroup`. If no :class:`Selection` is specified, all errors will match. Make sure to only omit
    :attr:`resubmit_errors` if this is the last :class:`ResubmissionDestination` in the :class:`FailurePolicy`,
    otherwise and proceeding :class:`ResubmissionDestination`\\s will be unreachable.

    The :class:`TaskErrorSelector` will be applied to the last seen error.
    """


# KEEP
def destination(*, toTaskGroup: str, when: Optional[Selection[TaskErrorSelector]] = None) -> ResubmissionDestination:
    return ResubmissionDestination(
        destinationTaskGroup=toTaskGroup,
        resubmitErrors=when
    )