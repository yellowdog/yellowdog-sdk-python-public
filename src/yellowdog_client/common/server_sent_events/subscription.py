from threading import Lock
from typing import Set, TypeVar, Type
from copy import deepcopy

from yellowdog_client.common import Closeable
from yellowdog_client.common.json import Json
from yellowdog_client.model.exceptions import InvalidOperationException
from .subscription_event_listener import SubscriptionEventListener
from .sse4python import EventSource
from .sse4python import ServerSentEvent

T = TypeVar('T')


class Subscription(Closeable):
    _sync_lock: Lock = None
    _id: str = None
    _listeners: Set[SubscriptionEventListener] = set()
    _event_source: EventSource = None

    def __init__(self, sse: EventSource, listener: SubscriptionEventListener, class_type: Type[T]) -> None:
        self._sync_lock = Lock()
        self._id = hex(hash(self))
        self._listeners = set()
        self._listeners.add(listener)
        self._class_type = class_type
        self._event_source = sse
        self._event_source.bind(event_received=self._receive_event)
        self._event_source.bind(error_received=self._notify_error)
        self._event_source.bind(event_source_completed=self._notify_server_cancelled)
        self._event_source.start()

    def __copy_listeners(self) -> Set[SubscriptionEventListener]:
        with self._sync_lock:
            return set(x for x in self._listeners)

    def _receive_event(self, message: ServerSentEvent) -> None:
        if message.data:
            data = Json.loads(message.data, self._class_type)
            for subscription_event_listener in self.__copy_listeners():
                try:
                    object_copy = deepcopy(data)
                    subscription_event_listener.updated(obj=object_copy)
                except Exception as ex:
                    print(str(ex))    # ignored. Failed to notify listeners for some reason

    def _notify_error(self, error: Exception) -> None:
        for subscription_event_listener in self.__copy_listeners():
            subscription_event_listener.subscription_error(error=error)

    def _notify_server_cancelled(self) -> None:
        for subscription_event_listener in self.__copy_listeners():
            subscription_event_listener.subscription_cancelled()

    def add_subscription_listener(self, listener: SubscriptionEventListener) -> None:
        if self._event_source.is_closed:
            raise InvalidOperationException("Subscription is not active")
        with self._sync_lock:
            self._listeners.add(listener)

    def remove_listener(self, listener: SubscriptionEventListener) -> None:
        with self._sync_lock:
            self._listeners.remove(listener)
            if len(self._listeners) < 1:
                self.close()

    def has_listener(self, listener: SubscriptionEventListener) -> bool:
        with self._sync_lock:
            return listener in self._listeners

    def is_closed(self) -> bool:
        return self._event_source.is_closed

    def close(self) -> None:
        self._event_source.stop()

