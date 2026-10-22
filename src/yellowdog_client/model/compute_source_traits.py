from dataclasses import dataclass


@dataclass
class ComputeSourceTraits:
    """Describes behavioural traits specific to a compute source."""
    canStopStart: bool = False
    canRestart: bool = False
    canScaleOut: bool = False
    isSelfMaintained: bool = False
    """Indicates if the compute source is responsible itself for maintaining its target instance count."""
