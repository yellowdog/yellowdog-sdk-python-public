from dataclasses import dataclass
from typing import Optional

from .configured_worker_pool import ConfiguredWorkerPool
from .worker_pool_token import WorkerPoolToken


@dataclass
class AddConfiguredWorkerPoolResponse:
    workerPool: Optional[ConfiguredWorkerPool] = None
    token: Optional[WorkerPoolToken] = None
