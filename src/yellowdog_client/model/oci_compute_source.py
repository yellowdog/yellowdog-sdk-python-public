from dataclasses import dataclass, field
from typing import Optional

from .cloud_provider import CloudProvider
from .compute_source import ComputeSource


@dataclass
class OciComputeSource(ComputeSource):
    """Derives from ComputeSource to provide the interface for all AWS compute source model objects."""
    type: str = field(default="co.yellowdog.platform.model.OciComputeSource", init=False)
    provider: Optional[CloudProvider] = field(default=None, init=False)
