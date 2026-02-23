from abc import ABC
from typing import Generic, Optional, TypeVar

TValue = TypeVar('TValue')



class AttributeValue(Generic[TValue], ABC):
    type: str
    attribute: Optional[str]
    value: Optional[TValue]
