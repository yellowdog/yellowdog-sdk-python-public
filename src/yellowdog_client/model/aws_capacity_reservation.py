from dataclasses import dataclass
from typing import Optional

from .aws_capacity_reservation_preference import AwsCapacityReservationPreference


@dataclass
class AwsCapacityReservation:
    preference: AwsCapacityReservationPreference
    groupArn: Optional[str] = None
    id: Optional[str] = None
