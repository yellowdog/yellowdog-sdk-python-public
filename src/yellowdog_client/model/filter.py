from abc import ABC
from datetime import datetime
from typing import Optional



class Filter(ABC):
    fromTime: Optional[datetime]
    untilTime: Optional[datetime]
