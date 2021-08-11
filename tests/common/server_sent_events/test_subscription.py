import sys

import pytest
import mock

from yellowdog_client.common.server_sent_events import Subscription
from yellowdog_client.common.server_sent_events.sse4python import EventSource
from yellowdog_client.common.server_sent_events import SubscriptionEventListener
from yellowdog_client.model.exceptions import InvalidOperationException
from yellowdog_client.common.server_sent_events.sse4python import ConnectingState


class ExampleObject(object):
    foo = None


class ExampleListener(SubscriptionEventListener):
    res_subscription_cancelled = None
    res_subscription_error = None
    res_updated = None

    def subscription_cancelled(self):
        self.res_subscription_cancelled = True

    def subscription_error(self, error):
        self.res_subscription_error = error

    def updated(self, obj):
        self.res_updated = obj


class SubscriptionFactoryFixture(object):
    @pytest.fixture
    def subscription_factory__no_listeners(self, subscription_factory__1_listener):
        subscription, event_source, removed_listener = subscription_factory__1_listener
        subscription._listeners = set()
        return subscription, event_source, removed_listener

    @pytest.fixture
    def subscription_factory__1_listener(self, mocker):
        mocker.patch("yellowdog_client.common.server_sent_events.sse4python.event_source.EventSource.start")
        event_source = EventSource(url=mocker.MagicMock, factory=mocker.MagicMock())
        listener = ExampleListener()
        subscription = Subscription(sse=event_source, listener=listener, class_type=mocker.MagicMock())
        return subscription, event_source, listener

    @pytest.fixture
    def subscription_factory__3_listeners(self, subscription_factory__1_listener):
        subscription, event_source, listener1 = subscription_factory__1_listener
        listener2 = ExampleListener()
        subscription.add_subscription_listener(listener=listener2)
        listener3 = ExampleListener()
        subscription.add_subscription_listener(listener=listener3)
        return subscription, event_source, listener1, listener2, listener3


class TestInit(object):
    def test__expect_id_assigned__listener_added__source_binded_and_started(self, mocker):
        hash_func = 'builtins.hash' if sys.version_info[0] >= 3 else '__builtin__.hash'
        with mock.patch(hash_func, lambda x: 999):
            mock_sse = mocker.MagicMock()
            mock_listener = mocker.MagicMock()

            subscription = Subscription(sse=mock_sse, listener=mock_listener, class_type=mocker.MagicMock())

            assert subscription._id == "0x3e7"
            assert len(subscription._listeners) == 1
            assert all(x == mock_listener for x in subscription._listeners)
            mock_sse.start.assert_called_once()


class TestNotifyServerCancelled(SubscriptionFactoryFixture):
    def test__not_cancelled_token__no_listeners__expect_event_source_cancelled_and_no_event_passed(
            self, subscription_factory__no_listeners):
        subscription, event_source, removed_listener = subscription_factory__no_listeners

        assert not event_source._token_source.cancelled

        thread = event_source._on_event_source_completed()
        thread.join()

        assert event_source._token_source.cancelled
        assert not removed_listener.res_subscription_cancelled

    def test__cancelled_token__no_listeners__expect_no_event_passed(self, subscription_factory__no_listeners):
        subscription, event_source, removed_listener = subscription_factory__no_listeners

        event_source._token_source.cancel()

        thread = event_source._on_event_source_completed()
        thread.join()

        assert event_source._token_source.cancelled
        assert not removed_listener.res_subscription_cancelled

    def test_1_listener__expect_event_passed(self, subscription_factory__1_listener):
        subscription, event_source, listener1 = subscription_factory__1_listener

        thread = event_source._on_event_source_completed()
        thread.join()

        assert listener1.res_subscription_cancelled

    def test_3_listeners__expect_event_passed(self, subscription_factory__3_listeners):
        subscription, event_source, listener1, listener2, listener3 = subscription_factory__3_listeners

        thread = event_source._on_event_source_completed()
        thread.join()

        assert listener1.res_subscription_cancelled
        assert listener2.res_subscription_cancelled
        assert listener3.res_subscription_cancelled


class TestNotifyError(SubscriptionFactoryFixture):
    def test__no_listeners__expect_no_event_passed(
            self, subscription_factory__no_listeners):
        subscription, event_source, removed_listener = subscription_factory__no_listeners

        thread = event_source._on_error_received(Exception("TESTING"))
        thread.join()

        assert removed_listener.res_subscription_error is None

    def test__3_listeners__expect_errors_passed(self, subscription_factory__3_listeners):
        subscription, event_source, listener1, listener2, listener3 = subscription_factory__3_listeners

        thread = event_source._on_error_received(Exception("TESTING"))
        thread.join()

        assert str(listener1.res_subscription_error) == "TESTING"
        assert str(listener2.res_subscription_error) == "TESTING"
        assert str(listener3.res_subscription_error) == "TESTING"


class TestReceiveEvent(SubscriptionFactoryFixture):
    def test__1_listener__no_raw_data__expect_nothing_passed(self, mocker, subscription_factory__1_listener):
        subscription, event_source, listener1 = subscription_factory__1_listener
        message = mocker.MagicMock()
        message.raw_data = None

        thread = event_source._on_event_received(sse=message)
        thread.join()

        assert listener1.res_updated is None

    def test__no_listener__raw_data__expect_no_listeners_notified(self, mocker, subscription_factory__no_listeners):
        subscription, event_source, removed_listener = subscription_factory__no_listeners
        message = mocker.MagicMock()
        message.raw_data = "RAW DATA"
        mock_deserialized_data = mocker.MagicMock()
        message.deserialize_data.return_value = mock_deserialized_data

        thread = event_source._on_event_received(sse=message)
        thread.join()

        assert removed_listener.res_updated is None

    def test__3_listeners__raw_data__expect_listeners_notified_with_unique_objects(
            self, mocker, subscription_factory__3_listeners):
        subscription, event_source, listener1, listener2, listener3 = subscription_factory__3_listeners
        message = mocker.MagicMock()
        message.raw_data = "RAW DATA"
        test_response = ExampleObject()
        test_response.foo = "bar"
        message.deserialize_data.return_value = test_response

        thread = event_source._on_event_received(sse=message)
        thread.join()

        assert listener1.res_updated.foo == listener2.res_updated.foo == listener3.res_updated.foo == "bar"
        assert listener1.res_updated != listener2.res_updated != listener3.res_updated
        assert test_response not in [listener1.res_updated, listener2.res_updated, listener3.res_updated]

    def __fail_method(self, _):
        raise ValueError("THIS CALLBACK FAILS")

    def test__3_listeners__one_fails__raw_data__expect_listeners_notified_with_unique_objects_and_silent_fail(
            self, mocker, subscription_factory__3_listeners):
        subscription, event_source, listener1, listener2, listener3 = subscription_factory__3_listeners
        message = mocker.MagicMock()
        message.raw_data = "RAW DATA"
        test_response = ExampleObject()
        test_response.foo = "bar"
        message.deserialize_data.return_value = test_response
        listener2.updated = self.__fail_method

        thread = event_source._on_event_received(sse=message)
        thread.join()

        assert listener1.res_updated.foo == listener3.res_updated.foo == "bar"
        assert listener2.res_updated is None
        assert listener1.res_updated != listener3.res_updated
        assert test_response not in [listener1.res_updated, listener3.res_updated]


class TestAddListener(SubscriptionFactoryFixture):
    def test__source_is_closed__expect_invalid_operation_exception(self, subscription_factory__no_listeners):
        subscription, event_source, removed_listener = subscription_factory__no_listeners
        event_source._token_source.cancel()

        with pytest.raises(InvalidOperationException):
            subscription.add_subscription_listener(listener=removed_listener)

        assert not subscription.has_listener(listener=removed_listener)

    def test__source_is_valid__expect_listener_added(self, subscription_factory__no_listeners):
        subscription, event_source, removed_listener = subscription_factory__no_listeners

        subscription.add_subscription_listener(listener=removed_listener)

        assert subscription.has_listener(listener=removed_listener)


class TestIsClosed(SubscriptionFactoryFixture):
    def test__source_token_is_cancelled__state_is_closed__expect_closed(self, subscription_factory__1_listener):
        subscription, event_source, listener = subscription_factory__1_listener
        event_source._token_source.cancel()

        assert subscription.is_closed()

    def test__source_token_is_not_cancelled__state_is_closed__expect_not_closed(self, subscription_factory__1_listener):
        subscription, event_source, listener = subscription_factory__1_listener

        assert not subscription.is_closed()

    def test__source_token_is_cancelled__state_is_not_closed__expect_not_closed(
            self, mocker, subscription_factory__1_listener):
        subscription, event_source, listener = subscription_factory__1_listener
        event_source._current_state = ConnectingState(url=mocker.MagicMock(), web_requester_factory=mocker.MagicMock())

        assert not subscription.is_closed()


class TestRemoveListener(SubscriptionFactoryFixture):
    def test__3_listeners__expect_listener_removed_and_no_close(self, subscription_factory__3_listeners):
        subscription, event_source, listener1, listener2, listener3 = subscription_factory__3_listeners
        assert subscription.has_listener(listener=listener2)

        subscription.remove_listener(listener=listener2)

        assert not subscription.has_listener(listener=listener2)
        assert not subscription.is_closed()

    def test__1_listeners__expect_listener_removed_and_source_closed(self, subscription_factory__1_listener):
        subscription, event_source, listener = subscription_factory__1_listener

        assert subscription.has_listener(listener=listener)
        assert not subscription.is_closed()

        subscription.remove_listener(listener=listener)

        assert not subscription.has_listener(listener=listener)
        assert subscription.is_closed()
