from abc import ABC
from typing import List, Optional

from .compute_source import ComputeSource



class ComputeProvisionStrategy(ABC):
    """
    The interface implemented by all compute provision strategy model objects.

    A compute provision strategy determines the behaviour of YellowDog Compute when trying to acquire and release instances to meet the compute requirement.
    """

    type: str
    sources: Optional[List[ComputeSource]]
    """Returns a list of the compute provision sources available for use by this provision strategy."""
