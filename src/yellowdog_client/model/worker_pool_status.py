from __future__ import annotations

from enum import Enum


class WorkerPoolStatus(Enum):
    """Indicates the status of a worker pool"""
    available: bool
    """
    Returns true, if the status indicates the pool is currently available (i.e. its workers can be claimed); otherwise, false.
    Nodes can register with the pool in any status until the pool has finished.
    """

    finished: bool
    """Returns true, if the status indicates the pool has finished and will do no further work; otherwise, false."""

    PENDING = "PENDING", True, False
    """The worker pool has just started, or just finished configuring its nodes. It becomes EMPTY, IDLE or RUNNING shortly afterwards, depending on its workers."""
    CONFIGURING = "CONFIGURING", False, False
    """The nodes in the worker pool are being identified and their node types are being set."""
    EMPTY = "EMPTY", True, False
    """The worker pool has no available workers, for example because none have registered yet or all have been lost."""
    IDLE = "IDLE", True, False
    """The worker pool has registered workers but none are currently claimed."""
    RUNNING = "RUNNING", True, False
    """One or more workers are claimed."""
    SHUTDOWN = "SHUTDOWN", False, True
    """The worker pool is shut down and its nodes are instructed to shut down."""
    TERMINATED = "TERMINATED", False, True
    """The worker pool is terminated and the associated compute requirement is terminated (provisioned worker pool) or all its nodes have become inactive, including any that have been lost (configured worker pool)."""

    def __new__(cls, value: str, available: bool, finished: bool) -> WorkerPoolStatus:
        obj = object.__new__(cls)
        obj._value_ = value
        obj.available = available
        obj.finished = finished
        return obj

    def __str__(self) -> str:
        return self.name
