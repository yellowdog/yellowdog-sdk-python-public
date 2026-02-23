from abc import ABC
from typing import ClassVar, Optional



class AttributePreference(ABC):
    DEFAULT_WEIGHT: ClassVar[int] = 1
    type: str
    attribute: Optional[str]
    weight: Optional[float]
