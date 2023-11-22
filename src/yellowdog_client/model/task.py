from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, List, Optional

from .flatten_path import FlattenPath
from .identified import Identified
from .named import Named
from .tagged import Tagged
from .task_error import TaskError
from .task_input import TaskInput
from .task_output import TaskOutput
from .task_status import TaskStatus


@dataclass
class Task(Identified, Named, Tagged):
    """Defines a task to be executed as part of a WorkRequirement."""
    id: Optional[str] = field(default=None, init=False)
    fullyQualifiedName: Optional[str] = field(default=None, init=False)
    """The system generated fully qualified name of the task in the form {namespace}/{workRequirementName}/{taskGroupName}/{taskName}. This is only generated if all ancestor entities are named."""
    status: Optional[TaskStatus] = field(default=None, init=False)
    """The task status."""
    retryCount: Optional[int] = field(default=None, init=False)
    """How many times the task has failed and then been set back to WAITING to be retried."""
    taskGroupId: Optional[str] = field(default=None, init=False)
    workerId: Optional[str] = field(default=None, init=False)
    errors: Optional[List[TaskError]] = field(default=None, init=False)
    taskType: str
    """The type of the task, used to identify the program to use to execute the task."""
    name: Optional[str] = None
    """The user allocated name used to uniquely identify the task within its task group."""
    tag: Optional[str] = None
    arguments: Optional[List[str]] = None
    """A list of arguments that will be passed to the task type run command when the task is executed."""
    taskData: Optional[str] = None
    """The data to be passed to the Worker when the task is started."""
    environment: Optional[Dict[str, str]] = None
    """A map containing environment variable values that will be added to the process environment when the task is executed."""
    startedTime: Optional[datetime] = None
    """The time the task was last started by a Worker."""
    finishedTime: Optional[datetime] = None
    """The time the task was finished."""
    abortRequestedTime: Optional[datetime] = None
    """The time when task abort was requested."""
    inputs: Optional[List[TaskInput]] = None
    """Input object specifications that determine objects to be downloaded prior to running the task."""
    flattenInputPaths: Optional[FlattenPath] = None
    """Indicates if the input objects' paths should be flattened when they are downloaded."""
    outputs: Optional[List[TaskOutput]] = None
    """Output object specifications that determine objects to be uploaded after running the task."""
    timeout: Optional[timedelta] = None
    """The maximum time that a worker should attempt to execute the task for before failing it."""
