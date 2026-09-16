from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from .cluster_operation_type import ClusterOperationType


@dataclass
class ClusterOperation:
    type: Optional[ClusterOperationType] = None
    createdTime: Optional[datetime] = None
    finishedTime: Optional[datetime] = None
    successful: Optional[bool] = None
    message: Optional[str] = None
