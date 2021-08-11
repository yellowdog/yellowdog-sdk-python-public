from dataclasses import dataclass
from typing import Generic, List, Optional, TypeVar

T = TypeVar('T')


@dataclass
class Slice(Generic[T]):
    items: Optional[List[T]] = None
    nextSliceId: Optional[str] = None
