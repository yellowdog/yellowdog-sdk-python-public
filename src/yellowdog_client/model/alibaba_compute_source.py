from dataclasses import dataclass, field

from .compute_source import ComputeSource


@dataclass
class AlibabaComputeSource(ComputeSource):
    """Derives from ComputeSource to provide the interface for all Alibaba Cloud compute source model objects."""
    type: str = field(default="co.yellowdog.platform.model.AlibabaComputeSource", init=False)
