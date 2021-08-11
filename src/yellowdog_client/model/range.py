from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar('T')


@dataclass
class Range(Generic[T]):
    pass
