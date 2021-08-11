import pytest
from yellowdog_client.common.server_sent_events import SubscriptionManager
from yellowdog_client.common.server_sent_events import Subscription
from yellowdog_client.model.exceptions import InvalidOperationException

SUBSCRIPTION_TYPE = "yellowdog_client.common.server_sent_events.subscription_manager.Subscription"


class TestCreateSubscription(object):
    def test__expect_subscription_appended_and_returned(self, mocker):
        obj = mocker.MagicMock()
        obj.id = "MY_ID"
        listener = mocker.MagicMock()

        manager = SubscriptionManager(update_events_provider=mocker.MagicMock(), class_type=mocker.MagicMock())

        res = manager.create_subscription(obj=obj, listener=listener)
        assert type(res) == Subscription
        assert res == manager._subscriptions["MY_ID"]


class TestAddListener(object):
    def test__no_id__expect_exception(self, mocker):
        obj = mocker.MagicMock()
        obj.id = None
        listener = mocker.MagicMock()

        manager = SubscriptionManager(update_events_provider=mocker.MagicMock(), class_type=mocker.MagicMock())

        with pytest.raises(InvalidOperationException):
            manager.add_listener(obj=obj, listener=listener)

    def test__no_subscription__expect_subscription_created(self, mocker):
        obj = mocker.MagicMock()
        obj.id = "ID1"
        listener = mocker.MagicMock()

        manager = SubscriptionManager(update_events_provider=mocker.MagicMock(), class_type=mocker.MagicMock())

        assert len(manager._subscriptions) == 0

        manager.add_listener(obj=obj, listener=listener)

        assert type(manager._subscriptions["ID1"]) == Subscription
        assert len(manager._subscriptions) == 1

    def test__non_matching_subscriptions__expect_subscription_created(self, mocker):
        obj1 = mocker.MagicMock()
        obj1.id = "ID1"
        listener1 = mocker.MagicMock()

        obj2 = mocker.MagicMock()
        obj2.id = "ID2"
        listener2 = mocker.MagicMock()

        manager = SubscriptionManager(update_events_provider=mocker.MagicMock(), class_type=mocker.MagicMock())
        manager.create_subscription(obj=obj2, listener=listener2)

        assert len(manager._subscriptions) == 1

        manager.add_listener(obj=obj1, listener=listener1)

        assert type(manager._subscriptions["ID1"]) == Subscription
        assert len(manager._subscriptions) == 2

    def test__matching_subscription__listener_is_none__expect_no_appending_to_existing_subscription(self, mocker):
        mock_subscription = mocker.patch(SUBSCRIPTION_TYPE)

        obj1 = mocker.MagicMock()
        obj1.id = "ID1"

        obj2 = mocker.MagicMock()
        obj2.id = "ID1"
        listener2 = mocker.MagicMock()

        manager = SubscriptionManager(update_events_provider=mocker.MagicMock(), class_type=mocker.MagicMock())
        manager.create_subscription(obj=obj2, listener=listener2)

        assert len(manager._subscriptions) == 1

        manager.add_listener(obj=obj1, listener=None)

        assert manager._subscriptions["ID1"] == mock_subscription.return_value
        assert len(manager._subscriptions) == 1
        mock_subscription.return_value.add_listener.assert_not_called()

    def test__matching_subscription__expect_appended_to_existing_subscription(self, mocker):
        mock_subscription = mocker.patch(SUBSCRIPTION_TYPE)

        obj1 = mocker.MagicMock()
        obj1.id = "ID1"
        listener1 = mocker.MagicMock()

        obj2 = mocker.MagicMock()
        obj2.id = "ID1"
        listener2 = mocker.MagicMock()

        manager = SubscriptionManager(update_events_provider=mocker.MagicMock(), class_type=mocker.MagicMock())
        manager.create_subscription(obj=obj2, listener=listener2)

        assert len(manager._subscriptions) == 1

        manager.add_listener(obj=obj1, listener=listener1)

        assert manager._subscriptions["ID1"] == mock_subscription.return_value
        assert len(manager._subscriptions) == 1
        mock_subscription.return_value.add_subscription_listener.assert_called_once_with(listener=listener1)


class TestRemoveListener(object):
    def test__no_subscriptions__expect_no_listeners_removed(self, mocker):
        listener = mocker.MagicMock()
        mock_subscription = mocker.patch(SUBSCRIPTION_TYPE)

        manager = SubscriptionManager(update_events_provider=mocker.MagicMock(), class_type=mocker.MagicMock())

        manager.remove_listener(listener=listener)

        mock_subscription.remove_listener.assert_not_called()

    def test__subscription_does_not_have_listener__expect_no_listeners_removed(self, mocker):
        listener = mocker.MagicMock()
        mock_subscription = mocker.MagicMock()
        mock_subscription.has_listener.return_value = False

        manager = SubscriptionManager(update_events_provider=mocker.MagicMock(), class_type=mocker.MagicMock())
        manager._subscriptions["SUB1"] = mock_subscription

        manager.remove_listener(listener=listener)

        mock_subscription.remove_listener.assert_not_called()

    def test__subscription_has_listener__expect_listener_removed(self, mocker):
        listener = mocker.MagicMock()
        mock_subscription = mocker.MagicMock()
        mock_subscription.has_listener.return_value = True

        manager = SubscriptionManager(update_events_provider=mocker.MagicMock(), class_type=mocker.MagicMock())
        manager._subscriptions["SUB1"] = mock_subscription

        manager.remove_listener(listener=listener)

        mock_subscription.remove_listener.assert_called_once_with(listener=listener)

    def test__2_subscriptions__one_is_closed__expect_only_1_checked(self, mocker):
        listener = mocker.MagicMock()
        mock_subscription_1 = mocker.MagicMock()
        mock_subscription_1.has_listener.return_value = False
        mock_subscription_1.is_closed.return_value = True
        mock_subscription_2 = mocker.MagicMock()

        manager = SubscriptionManager(update_events_provider=mocker.MagicMock(), class_type=mocker.MagicMock())
        manager._subscriptions["1"] = mock_subscription_1
        manager._subscriptions["2"] = mock_subscription_2

        manager.remove_listener(listener=listener)

        mock_subscription_2.has_listener.assert_not_called()
        mock_subscription_2.has_listener.is_closed()


class TestClose(object):
    def test__expect_all_subscriptions_closed_and_dictionary_cleared(self, mocker):
        mock_subscription_1 = mocker.MagicMock()
        mock_subscription_2 = mocker.MagicMock()

        manager = SubscriptionManager(update_events_provider=mocker.MagicMock(), class_type=mocker.MagicMock())
        manager._subscriptions["1"] = mock_subscription_1
        manager._subscriptions["2"] = mock_subscription_2

        manager.close()

        mock_subscription_1.close.assert_called_once()
        mock_subscription_2.close.assert_called_once()
        assert manager._subscriptions == {}
