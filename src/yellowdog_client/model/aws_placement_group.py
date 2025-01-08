from dataclasses import dataclass
from typing import Optional


@dataclass
class AwsPlacementGroup:
    groupName: Optional[str] = None
    groupId: Optional[str] = None
