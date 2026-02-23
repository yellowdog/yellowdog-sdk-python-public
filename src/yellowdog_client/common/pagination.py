from typing import TypeVar, Callable, List

from yellowdog_client.model import SliceReference, Slice

T = TypeVar('T')


def paginate(slice_loader: Callable[[SliceReference], Slice[T]]) -> List[T]:
    slice = slice_loader(SliceReference())
    items = slice.items or []

    while slice.nextSliceId is not None:
        slice = slice_loader(SliceReference(slice.nextSliceId))
        items += slice.items or []

    return items

