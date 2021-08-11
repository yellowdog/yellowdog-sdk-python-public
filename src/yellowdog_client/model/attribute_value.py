from dataclasses import dataclass, field
from typing import Generic, TypeVar

TValue = TypeVar('TValue')


@dataclass
class AttributeValue(Generic[TValue]):
    type: str = field(default=None, init=False)
