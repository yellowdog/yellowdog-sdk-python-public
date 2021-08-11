from dataclasses import dataclass


@dataclass
class ComputeRequirementSupportedOperations:
    """Describes operations supported by a Compute Requirement based the traits of its compute sources."""
    canStopStart: bool = False
    canScaleOut: bool = False
    canReprovision: bool = False
