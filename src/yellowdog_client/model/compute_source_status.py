from enum import Enum


class ComputeSourceStatus(Enum):
    """
    Describes the status of a compute source.

    The status of a compute source indicates if there are active instances from that source, or if the source is currently being changed or has errored.
    """

    NEW = "NEW"
    """The compute source has been created and submitted to YellowDog Compute."""
    INACTIVE = "INACTIVE"
    """The compute source is either not providing any instances or any that have been provided are now terminated."""
    ACTIVE = "ACTIVE"
    """The compute source is providing at least one instance that is not terminated."""
    UPDATING = "UPDATING"
    """YellowDog Compute is currently updating its usage of the compute source. This could be provisioning or deprovisioning instances, or transitioning instances (stopping, starting, restarting, terminating)"""
    ERRORED = "ERRORED"
    """The last requested action performed by YellowDog Compute with this compute source resulted in an error."""

    def __str__(self) -> str:
        return self.name
