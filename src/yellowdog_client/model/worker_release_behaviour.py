from enum import Enum


class WorkerReleaseBehaviour(Enum):
    """Indicates the behaviour that the YellowDog Scheduler should apply when releasing workers from a task group."""
    NO_PENDING_TASKS = "NO_PENDING_TASKS"
    """Workers not currently executing tasks for the task group are released as soon as no further tasks are PENDING."""
    ALL_TASKS_FINISHED = "ALL_TASKS_FINISHED"
    """All workers are released but only once all tasks in the task group are finished (COMPLETED, or FAILED)."""
    WORK_REQUIREMENT_FINISHED = "WORK_REQUIREMENT_FINISHED"
    """Workers are only released from the task group when the containing work requirement is finished."""

    def __str__(self) -> str:
        return self.name
