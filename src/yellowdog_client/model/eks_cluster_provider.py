from dataclasses import dataclass, field
from typing import List

from .cluster_provider import ClusterProvider


@dataclass
class EksClusterProvider(ClusterProvider):
    type: str = field(default="co.yellowdog.platform.model.EksClusterProvider", init=False)
    region: str
    clusterRoleArn: str
    nodeRoleArn: str
    subnetIds: List[str]
    securityGroups: List[str]
    lambdaArn: str
    lambdaRoleArn: str
