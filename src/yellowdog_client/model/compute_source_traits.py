from dataclasses import dataclass


@dataclass
class ComputeSourceTraits:
    """Describes behavioural traits specific to a compute source."""
    canStopStart: bool = False
    canRestart: bool = False
    canScaleOut: bool = False
    isSelfMaintained: bool = False
