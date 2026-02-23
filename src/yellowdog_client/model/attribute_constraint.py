from abc import ABC
from typing import Optional



class AttributeConstraint(ABC):
    type: str
    attribute: Optional[str]
