from dataclasses import dataclass
from typing import Set

from .instant_range import InstantRange


@dataclass
class MeasurementSearch:
    metrics: Set[str]
    timestamp: InstantRange
