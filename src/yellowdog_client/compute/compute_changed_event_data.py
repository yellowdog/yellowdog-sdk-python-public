from typing import List

from yellowdog_client.model import ComputeRequirement
from yellowdog_client.model import Instance


class ComputeChangedEventData(object):
    compute_requirement = None  # type: ComputeRequirement
    changed_instances = None  # type: List[Instance]

    def __init__(self, compute_requirement, changed_instances):
        # type: (ComputeRequirement, List[Instance]) -> None
        self.compute_requirement = compute_requirement
        self.changed_instances = changed_instances
