from enum import Enum


class InstanceStatus(Enum):
    """Describes the status of a computer machine instance."""
    PENDING = "PENDING"
    """The instance is in the process of being provisioned, or rebooted."""
    RUNNING = "RUNNING"
    """The instance is running."""
    STOPPING = "STOPPING"
    """The instance is in the process of being stopped."""
    STOPPED = "STOPPED"
    """The instance has been stopped."""
    TERMINATING = "TERMINATING"
    """The instance is in the process of being terminated."""
    TERMINATED = "TERMINATED"
    """The instance has been terminated and can no longer be used."""
    UNAVAILABLE = "UNAVAILABLE"
    """The instance is unavailable due to a process external to YellowDog e.g. creating an image or repairing the instance."""
    UNKNOWN = "UNKNOWN"
    """The status of the instance is unknown. The instance can be restarted to try to recover or terminated."""

    def is_alive(self) -> bool:
        return self in (self.PENDING, self.RUNNING, self.STOPPING, self.STOPPED)

    def __str__(self) -> str:
        return self.name
