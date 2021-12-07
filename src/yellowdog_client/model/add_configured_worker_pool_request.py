from dataclasses import dataclass
from datetime import timedelta
from typing import Optional

from .configured_worker_pool_properties import ConfiguredWorkerPoolProperties


@dataclass
class AddConfiguredWorkerPoolRequest:
    name: str
    """The name used to uniquely identify the worker pool."""
    tokenTtl: Optional[timedelta] = None
    """
    The time-to-live of the worker pool token. Workers have this much time, from the creation of the worker token,
    to register. If not set, workers have an unlimited length of time to register.
    """

    properties: Optional[ConfiguredWorkerPoolProperties] = None
