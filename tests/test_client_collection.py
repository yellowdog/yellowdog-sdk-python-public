import pytest

from yellowdog_client.client_collection import ClientCollection


class TestClientCollection(object):
    def test__add__expect_added_value_returned(self, mocker):
        closable = mocker.patch("yellowdog_client.common.Closeable")
        collection = ClientCollection()
        res = collection.add(closable)
        assert closable == res

    def test__close__expect_inners_closed(self, mocker):
        closable = mocker.patch("yellowdog_client.common.Closeable")
        collection = ClientCollection()
        collection.add(closable)
        collection.close()
        closable.close.assert_called_once()

    def test__exception_occurs__expect_inners_still_closed(self, mocker):
        closable = mocker.patch("yellowdog_client.common.Closeable")

        with ClientCollection() as collection:
            collection.add(closable)
            with pytest.raises(Exception):
                raise Exception()

        closable.close.assert_called_once()
