from dataclasses import dataclass
from datetime import timedelta
from typing import List, Optional

from .cloud_provider import CloudProvider
from .double_range import DoubleRange


@dataclass
class RunSpecification:
    """Specifies the behaviours to be used by the YellowDog Scheduler when executing Tasks within the associated TaskGroup."""
    taskTypes: List[str]
    """The task types that will be used in the associated TaskGroup."""
    instanceTypes: Optional[List[str]] = None
    """The machine instance types that can be used to execute tasks"""
    vcpus: Optional[DoubleRange] = None
    """Range constraint on number of vCPUs that are required to execute tasks"""
    ram: Optional[DoubleRange] = None
    """Range constraint on GB of RAM that are required to execute tasks"""
    minWorkers: Optional[int] = None
    """The minimum number of Workers that the associated TaskGroup requires. This many workers must be claimed before the associated TaskGroup will start running."""
    maxWorkers: Optional[int] = None
    """The maximum number of Workers that can be claimed for the associated TaskGroup."""
    tasksPerWorker: Optional[int] = None
    """Determines the number of worker claims based on splitting the number of unfinished tasks across workers."""
    exclusiveWorkers: Optional[bool] = None
    """If true, then do not allow claimed Workers to be shared with other task groups; otherwise, Workers can be shared."""
    maximumTaskRetries: int = 0
    """The maximum number of times a task can be retried after it has failed."""
    taskTimeout: Optional[timedelta] = None
    """
    The maximum time that a worker should attempt to execute a task for before failing it.
    NB: This value can be overridden on individual tasks when they are added.
    """

    providers: Optional[List[CloudProvider]] = None
    """Constrains the YellowDog Scheduler to only execute tasks from the associated TaskGroup on the specified providers."""
    regions: Optional[List[str]] = None
    """Constrains the YellowDog Scheduler to only execute tasks from the associated TaskGroup in the specified regions."""
    workerTags: Optional[List[str]] = None
    """Constrains the YellowDog Scheduler to only execute tasks from the associated TaskGroup on workers with a matching tag value."""
