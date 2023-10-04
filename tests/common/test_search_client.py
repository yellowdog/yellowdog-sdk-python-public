from typing import List

import pytest

from yellowdog_client.common import SearchClient
from yellowdog_client.model import Slice, SliceReference

data_source: List[str] = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]


@pytest.fixture
def search_client() -> SearchClient[str]:
    return SearchClient(lambda slice_reference: get(slice_reference))


def test_list(search_client: SearchClient[str]):
    result = search_client.list_all()

    assert result == data_source


def test_iterate(search_client: SearchClient[str]):
    i = 0
    for item in search_client.iterate():
        assert item is data_source[i]
        i += 1

    assert i is len(data_source)


def get(slice_reference: SliceReference) -> Slice[str]:

    if slice_reference.sliceId is None:
        return Slice(items=data_source[0:3], nextSliceId="slice-reference-1")
    if slice_reference.sliceId == "slice-reference-1":
        return Slice(items=data_source[3:6], nextSliceId="slice-reference-2")
    if slice_reference.sliceId == "slice-reference-2":
        return Slice(items=data_source[6:9], nextSliceId=None)
