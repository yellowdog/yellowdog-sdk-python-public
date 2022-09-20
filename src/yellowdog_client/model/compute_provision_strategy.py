from dataclasses import dataclass, field


@dataclass
class ComputeProvisionStrategy:
    """
    The interface implemented by all compute provision strategy model objects.

    A compute provision strategy determines the behaviour of YellowDog Compute when trying to acquire and release instances to meet the compute requirement.
    """

    type: str = field(default=None, init=False)
