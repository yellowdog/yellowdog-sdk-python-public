from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from .compute_source_exhaustion_status import ComputeSourceExhaustionStatus


@dataclass
class ComputeSourceExhaustion:
    """Provides details for a compute source that is exhausted or nearing exhaustion."""
    status: Optional[ComputeSourceExhaustionStatus] = None
    """If the source is associated with an exhausted allowance, gets the exhaustion status."""
    expectedTermination: Optional[datetime] = None
    """The expected termination time when an associated exhausted allowance's hard limit grace period will expire."""
