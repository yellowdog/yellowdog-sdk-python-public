from dataclasses import dataclass
from typing import Optional

from .currency import Currency


@dataclass
class Price:
    currency: Optional[Currency] = None
    value: Optional[float] = None
