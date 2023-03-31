from collections.abc import Iterator
from typing import TypeVar, Callable, Optional, List, Generic

from yellowdog_client.model import Slice, SliceReference

T = TypeVar('T')


class SliceIterator(Generic[T], Iterator):

    def __init__(self, get_next_slice_function: Callable[[SliceReference], Slice[T]]):
        self.__get_next_slice_function: Callable[[SliceReference], Slice[T]] = get_next_slice_function
        self.__loaded: List[T] = []
        self.__next_slice_reference: Optional[SliceReference] = SliceReference()

    def __next__(self) -> T:
        # If there are elements or load completes successfully
        if not (len(self.__loaded) == 0) or self._load():
            return self.__loaded.pop(0)

        raise StopIteration

    def _load(self) -> bool:
        if self.__next_slice_reference is None:
            return False

        new_slice: Slice[T] = self.__get_next_slice_function(self.__next_slice_reference)

        if len(new_slice.items) == 0:
            self.__next_slice_reference = None
            return False

        if new_slice.nextSliceId is not None:
            self.__next_slice_reference = SliceReference(new_slice.nextSliceId)
        else:
            self.__next_slice_reference = None

        self.__loaded = new_slice.items

        return True
