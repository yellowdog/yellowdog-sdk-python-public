from dataclasses import dataclass
from typing import Dict, Optional

from .worker_pool_status import WorkerPoolStatus


@dataclass
class WorkerPoolDashboardSummary:
    statusCounts: Optional[Dict[WorkerPoolStatus, int]] = None
    errors: bool = False
