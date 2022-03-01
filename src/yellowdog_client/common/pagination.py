from typing import TypeVar, Callable

from yellowdog_client.model import SliceReference, Slice

T = TypeVar('T')


def paginate(slice_loader: Callable[[SliceReference], Slice[T]]):
    slice = slice_loader(SliceReference())
    items = slice.items

    while slice.nextSliceId is not None:
        slice = slice_loader(SliceReference(slice.nextSliceId))
        items += slice.items

    return items


def with_slice_reference(object: T, slice_reference: SliceReference) -> T:
    object.sliceReference = slice_reference
    return object
