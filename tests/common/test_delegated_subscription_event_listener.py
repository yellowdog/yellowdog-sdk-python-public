import pytest

from yellowdog_client.common.server_sent_events import DelegatedSubscriptionEventListener


class TestDelegatedSubscriptionEventListener(object):
    @pytest.fixture
    def callback_fixture(self):
        self.__callback_called = False

    def assert_true(self):
        assert True
        self.__callback_called = True

    def assert_obj(self, obj):
        assert obj == "TEST"
        self.__callback_called = True

    def test__update__expect_callback_invoked(self, callback_fixture):
        listener = DelegatedSubscriptionEventListener(on_update=self.assert_obj, on_error=None, on_cancel=None)
        listener.updated(obj="TEST")
        assert self.__callback_called

    def test__subscription_error__expect_callback_invoked(self, callback_fixture):
        listener = DelegatedSubscriptionEventListener(on_update=None, on_error=self.assert_obj, on_cancel=None)
        listener.subscription_error(error="TEST")
        assert self.__callback_called

    def test__subscription_cancelled__expect_callback_invoked(self, callback_fixture):
        listener = DelegatedSubscriptionEventListener(on_update=None, on_error=None, on_cancel=self.assert_true)
        listener.subscription_cancelled()
        assert self.__callback_called
