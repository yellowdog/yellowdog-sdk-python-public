from enum import Enum


class WorkerAction(Enum):
    """Indicates the type of action that a worker has been instructed to perform"""
    DO_TASK = "DO_TASK"
    """The worker has been instructed to execute a Task"""
    SLEEP = "SLEEP"
    """The worker has been instructed to sleep for a specified period of time. No longer used."""
    STOP = "STOP"
    """The worker has been instructed to stop"""
    SHUTDOWN = "SHUTDOWN"
    """The worker has been instructed to shutdown. No longer used."""

    def __str__(self) -> str:
        return self.name
