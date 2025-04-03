from dataclasses import dataclass
from typing import List, Optional

from .task_data_input import TaskDataInput
from .task_data_output import TaskDataOutput


@dataclass
class TaskData:
    inputs: Optional[List[TaskDataInput]] = None
    outputs: Optional[List[TaskDataOutput]] = None
