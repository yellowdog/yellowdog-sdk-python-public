from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from .cluster_provider import ClusterProvider
from .cluster_status import ClusterStatus
from .identified import Identified


@dataclass
class Cluster(Identified):
    """// A set of instances that work together to run applications."""
    id: Optional[str] = None
    namespace: Optional[str] = None
    name: Optional[str] = None
    clusterProvider: Optional[ClusterProvider] = None
    credential: Optional[str] = None
    status: Optional[ClusterStatus] = None
    createdTime: Optional[datetime] = None
    statusChangedTime: Optional[datetime] = None
