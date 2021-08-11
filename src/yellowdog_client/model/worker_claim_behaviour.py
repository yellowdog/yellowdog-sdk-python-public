from enum import Enum


class WorkerClaimBehaviour(Enum):
    """Indicates the behaviour that the YellowDog Scheduler should apply when claiming workers for a task group"""
    STARTUP_ONLY = "STARTUP_ONLY"
    """Once a task group has been started then do not try and claim any more workers"""
    MAINTAIN_IDEAL = "MAINTAIN_IDEAL"
    """Periodically check the number of workers claimed by a task group and attempt to claim more if less than the ideal count"""

    def __str__(self) -> str:
        return self.name
