from dataclasses import dataclass, field

from .compute_source import ComputeSource


@dataclass
class GceComputeSource(ComputeSource):
    """Derives from ComputeSource to provide the interface for all Google Compute Engine (GCE) compute source model objects."""
    type: str = field(default="co.yellowdog.platform.model.GceComputeSource", init=False)
