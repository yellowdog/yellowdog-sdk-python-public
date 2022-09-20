from enum import Enum


class InstanceStatus(Enum):
    """Describes the status of a instance."""
    PENDING = "PENDING", True
    """The instance is in the process of being provisioned, or rebooted."""
    RUNNING = "RUNNING", True
    """The instance is running."""
    STOPPING = "STOPPING", True
    """The instance is in the process of being stopped."""
    STOPPED = "STOPPED", True
    """The instance has been stopped."""
    TERMINATING = "TERMINATING", False
    """The instance is in the process of being terminated."""
    TERMINATED = "TERMINATED", False
    """The instance has been terminated and can no longer be used."""
    UNAVAILABLE = "UNAVAILABLE", False
    """The instance is unavailable due to a process external to YellowDog e.g. creating an image or repairing the instance."""
    UNKNOWN = "UNKNOWN", False
    """The status of the instance is unknown. The instance can be restarted to try to recover or terminated."""

    def __new__(cls, value, alive: bool):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.alive = alive
        return obj

    def __str__(self) -> str:
        return self.name
