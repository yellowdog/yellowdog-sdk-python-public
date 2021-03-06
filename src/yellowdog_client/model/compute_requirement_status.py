from enum import Enum


class ComputeRequirementStatus(Enum):
    """
    Describes the status of a compute requirement.

    The status of a compute requirement provides an aggregated view of the statuses of compute machine instances provisioned for that requirement.
    """

    NEW = "NEW"
    """The compute requirement has been created and submitted to YellowDog Compute."""
    PENDING = "PENDING"
    """
    YellowDog Compute is in the process of provisioning compute machine instances to meet the requirement.
    The requirement will remain in PENDING state until all newly provisioned instances have transitioned to RUNNING or TERMINATED (in the case where a provider cancels provision).
    """

    STARTING = "STARTING"
    """
    The computer machine instances provisioned for the requirement are being re-started after having been stopped.
    Some instances may already have started, however the requirement is still considered to be STARTING until all instances have started.
    """

    RUNNING = "RUNNING"
    """
    The computer machine instances provisioned for the requirement are running.
    Individual instances may be independently transitioned to other states but the requirement is still considered to be running.
    """

    STOPPING = "STOPPING"
    """
    The computer machine instances provisioned for the requirement are being stopped.
    Some instances may already have stopped, however the requirement is still considered to be STOPPING until all instances have stopped.
    """

    STOPPED = "STOPPED"
    """The computer machine instances provisioned for the requirement have stopped."""
    TERMINATING = "TERMINATING"
    """
    The computer machine instances provisioned for the requirement are being terminated.
    Some instances may already be terminated, however the requirement is still considered to be TERMINATING until all instances have terminated.
    """

    TERMINATED = "TERMINATED"
    """
    The computer machine instances provisioned for the requirement have been terminated.
    At this point the compute requirement may no longer be changed and is considered to be in a final state.
    """

    def __str__(self) -> str:
        return self.name
