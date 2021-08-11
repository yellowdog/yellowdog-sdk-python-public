from dataclasses import dataclass, field
from typing import Optional

from .cloud_provider import CloudProvider
from .compute_source import ComputeSource


@dataclass
class AlibabaComputeSource(ComputeSource):
    """Derives from ComputeSource to provide the interface for all Alibaba Cloud compute source model objects."""
    type: str = field(default="co.yellowdog.platform.model.AlibabaComputeSource", init=False)
    provider: Optional[CloudProvider] = field(default=None, init=False)
