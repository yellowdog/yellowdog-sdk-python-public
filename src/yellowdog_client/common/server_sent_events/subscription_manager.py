from typing import Callable, Dict, TypeVar
from threading import Lock

from .sse4python import EventSource
from .subscription import Subscription
from .subscription_event_listener import SubscriptionEventListener
from yellowdog_client.common import Closeable
from yellowdog_client.model import Identified
from yellowdog_client.model import ComputeRequirement
from yellowdog_client.model import WorkRequirement

IIdentified = TypeVar('IIdentified', Identified, ComputeRequirement, WorkRequirement)


class SubscriptionManager(Closeable):
    _sync_lock: Lock = None
    _update_events_provider: Callable[[str], EventSource] = None
    _class_type: type = None
    _subscriptions: Dict[str, Subscription] = None

    def __init__(self, update_events_provider: Callable[[str], EventSource], class_type: type) -> None:
        self._sync_lock = Lock()
        self._update_events_provider = update_events_provider
        self._class_type = class_type
        self._subscriptions = {}

    def create_subscription(self, id: str, listener: SubscriptionEventListener) -> Subscription:
        sse = self._update_events_provider(id)
        subscription = Subscription(sse=sse, listener=listener, class_type=self._class_type)
        self._subscriptions[id] = subscription
        return subscription

    @staticmethod
    def add_to_subscription(subscription: Subscription, listener: SubscriptionEventListener) -> Subscription:
        if listener is not None:
            subscription.add_subscription_listener(listener=listener)
        return subscription

    def add_listener(self, id: str, listener: SubscriptionEventListener) -> None:
        with self._sync_lock:
            if id in self._subscriptions:
                existing_subscription = self._subscriptions[id]
                self.add_to_subscription(subscription=existing_subscription, listener=listener)
            else:
                self.create_subscription(id, listener)

    def remove_listener(self, listener: SubscriptionEventListener) -> None:
        with self._sync_lock:
            for subscription_key in self._subscriptions:
                subscription = self._subscriptions[subscription_key]
                if subscription.has_listener(listener=listener):
                    subscription.remove_listener(listener=listener)
                if subscription.is_closed():
                    break

    def close(self) -> None:
        for object_id in self._subscriptions:
            self._subscriptions[object_id].close()
        self._subscriptions.clear()
