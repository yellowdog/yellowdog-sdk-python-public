from typing import TypeVar, Generic, Callable, List

from yellowdog_client.model import SliceReference, Slice
from .slice_iterator import SliceIterator

T = TypeVar('T')


class SearchClient(Generic[T]):

    def __init__(self, get_next_slice_function: Callable[[SliceReference], Slice[T]]):
        self.__get_next_slice_function: Callable[[SliceReference], Slice[T]] = get_next_slice_function

    def slice(self, slice_reference: SliceReference) -> Slice[T]:
        """
        Retrieve a slice of items from a given point & with a given size defined by a slice reference.
        :param slice_reference: the slice reference
        :return: a slice of items from the given point
        """
        return self.__get_next_slice_function(slice_reference)

    def list_all(self) -> List[T]:
        """
        Lists all the items.
        Warning: This method will automatically iterate over all response slices. See the slice method for
        more control.
        :return: a list of all items
        """
        return list(self.iterate())

    def iterate(self) -> SliceIterator[T]:
        """
        Iterates over all the items.
        Warning: This method will iterate over all response slices, loading slices when required by the iterator.
        See the slice method for more control.
        :return: an iterator for all items
        """
        return SliceIterator(self.__get_next_slice_function)
