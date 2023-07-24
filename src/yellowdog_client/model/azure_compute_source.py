from dataclasses import dataclass, field

from .compute_source import ComputeSource


@dataclass
class AzureComputeSource(ComputeSource):
    """Derives from ComputeSource to provide the interface for all Azure compute source model objects."""
    type: str = field(default="co.yellowdog.platform.model.AzureComputeSource", init=False)
