from copy import deepcopy
from typing import TypeVar, Optional

from .subscription_event_listener import SubscriptionEventListener

T = TypeVar('T')


class TrackingSubscriptionEventListener(SubscriptionEventListener):
    __previous: Optional[T] = None

    def __init__(self):
        self.__previous = None

    def _tracking_initialised(self, obj: T) -> None:
        """
        Invoked when this listener receives the first compute requirement event.

        :param obj: the first received instance of the object
        """

        raise NotImplementedError("_tracking_initialised Needs implementation")

    def _changed(self, previous: T, latest: T) -> None:
        """
        Invoked on each object event received following the first one

        :param previous: the previous instance of the object
        :param latest: the latest instance of the object
        """
        raise NotImplementedError("_changed Needs implementation")

    def updated(self, obj: T) -> None:
        if obj is None:
            return

        copy = deepcopy(obj)
        try:
            if self.__previous is None:
                self._tracking_initialised(obj=obj)
            else:
                self._changed(previous=self.__previous, latest=obj)
        finally:
            self.__previous = copy

    def subscription_error(self, error: Exception) -> None:
        raise NotImplementedError("subscription_error Needs implementation")

    def subscription_cancelled(self) -> None:
        raise NotImplementedError("subscription_cancelled Needs implementation")

