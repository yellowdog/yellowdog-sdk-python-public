from dataclasses import dataclass
from typing import TypeVar, Generic, List

from .pageable import Pageable
from .sort import Sort

T = TypeVar('T')


@dataclass
class Page(Generic[T]):
    content: List[T]
    empty: bool
    first: bool
    last: bool
    number: int
    numberOfElements: int
    pageable: Pageable
    size: int
    sort: Sort
    totalElements: int
    totalPages: int
