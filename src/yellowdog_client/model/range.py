from abc import ABC
from typing import Generic, Optional, TypeVar

T = TypeVar('T')



class Range(Generic[T], ABC):
    min: Optional[T]
    max: Optional[T]
