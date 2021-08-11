from typing import Callable, Dict, TypeVar
from threading import Lock

from .sse4python import EventSource
from .subscription import Subscription
from .subscription_event_listener import SubscriptionEventListener
from yellowdog_client.common import Closeable
from yellowdog_client.model import Identified
from yellowdog_client.model import ComputeRequirement
from yellowdog_client.model import WorkRequirement
from yellowdog_client.model.exceptions import InvalidOperationException

IIdentified = TypeVar('IIdentified', Identified, ComputeRequirement, WorkRequirement)


class SubscriptionManager(Closeable):
    _sync_lock = None  # type: Lock
    _update_events_provider = None  # type: Callable[[IIdentified], EventSource]
    _class_type = None  # type: type
    _subscriptions = None  # type: Dict[str, Subscription]

    def __init__(self, update_events_provider, class_type):
        # type: (Callable[[IIdentified], EventSource], type) -> None
        self._sync_lock = Lock()
        self._update_events_provider = update_events_provider
        self._class_type = class_type
        self._subscriptions = {}

    def create_subscription(self, obj, listener):
        # type: (IIdentified, SubscriptionEventListener) -> Subscription
        sse = self._update_events_provider(obj)
        subscription = Subscription(sse=sse, listener=listener, class_type=self._class_type)
        self._subscriptions[obj.id] = subscription
        return subscription

    @staticmethod
    def add_to_subscription(subscription, listener):
        # type: (Subscription, SubscriptionEventListener) -> Subscription
        if listener is not None:
            subscription.add_subscription_listener(listener=listener)
        return subscription

    def add_listener(self, obj, listener):
        # type: (IIdentified, SubscriptionEventListener) -> None
        if not obj.id:
            raise InvalidOperationException("Cannot add a listener for an object with null ID")

        with self._sync_lock:
            if obj.id in self._subscriptions:
                existing_subscription = self._subscriptions[obj.id]
                self.add_to_subscription(subscription=existing_subscription, listener=listener)
            else:
                self.create_subscription(obj=obj, listener=listener)

    def remove_listener(self, listener):
        # type: (SubscriptionEventListener) -> None
        with self._sync_lock:
            for subscription_key in self._subscriptions:
                subscription = self._subscriptions[subscription_key]
                if subscription.has_listener(listener=listener):
                    subscription.remove_listener(listener=listener)
                if subscription.is_closed():
                    break

    def close(self):
        # type: () -> None
        for object_id in self._subscriptions:
            self._subscriptions[object_id].close()
        self._subscriptions.clear()
