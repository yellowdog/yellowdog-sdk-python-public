from dataclasses import dataclass
from typing import Optional

from .cluster_provider import ClusterProvider


@dataclass
class ClusterSpec:
    """// A specification to provision a :class:`Cluster` from a :class:`ClusterProvider`."""
    namespace: str
    name: str
    clusterProvider: ClusterProvider
    credential: str
    connectorImageVersion: Optional[str] = None
