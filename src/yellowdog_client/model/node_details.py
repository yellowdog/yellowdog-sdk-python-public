from dataclasses import dataclass
from typing import List, Optional

from .cloud_provider import CloudProvider


@dataclass
class NodeDetails:
    """Describes the details of a worker pool node."""
    instanceId: str
    """The ID of the node's instance."""
    provider: Optional[CloudProvider] = None
    """The provider of the node's instance."""
    region: Optional[str] = None
    """The region in which the node's instance is running."""
    sourceName: Optional[str] = None
    """The name of the compute source from which the node's instance was provisioned."""
    sourceNumber: Optional[int] = None
    """The number of the compute source based on its order within the parent compute requirement."""
    instanceType: Optional[str] = None
    """The instance type of the instance."""
    hostname: Optional[str] = None
    """The hostname of the instance."""
    privateIpAddress: Optional[str] = None
    """The private IP address of the instance."""
    publicIpAddress: Optional[str] = None
    """The public IP address of the instance."""
    vcpus: Optional[float] = None
    """The number of processors (threads) on the node's instance."""
    ram: Optional[float] = None
    """The amount of RAM in GB on the node's instance."""
    supportedTaskTypes: Optional[List[str]] = None
    """The task types supported by this node."""
    workerTag: Optional[str] = None
    """An optional tag value that can be used to constrain worker allocation."""
    nodeType: Optional[str] = None
    """The node type of this node if node types have been configured."""
    nodeSlot: Optional[int] = None
    """The slot number of this node within its node type if slot numbering has been configured."""
