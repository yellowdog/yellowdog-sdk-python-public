from enum import Enum


class WorkerAction(Enum):
    """Indicates the type of action that a worker has been instructed to perform"""
    DO_TASK = "DO_TASK"
    """The worker has been instructed to execute a Task"""
    SLEEP = "SLEEP"
    """The worker has been instructed to sleep for a specified period of time"""
    SHUTDOWN = "SHUTDOWN"
    """The worker has been instructed to shutdown"""

    def __str__(self) -> str:
        return self.name
