from typing import Callable, TypeVar

from .subscription_event_listener import SubscriptionEventListener

T = TypeVar('T')


class DelegatedSubscriptionEventListener(SubscriptionEventListener):
    """
    Simple callback listener

    Constructor accepts the following **arguments**:

    :param on_update: mandatory. Callback for object updates
    :param on_error: optional. Callback for exceptions, received from the ``server sent events``
    :param on_cancel: optional. Callback for listener cancellation events
    """

    __on_update: Callable[[T], None] = None
    __on_error: Callable[[Exception], None] = None
    __on_cancel: Callable[[], None] = None

    def __init__(
            self,
            on_update: Callable[[T], None],
            on_error: Callable[[Exception], None] = None,
            on_cancel: Callable[[], None] = None
    ) -> None:
        self.__on_update = on_update
        self.__on_error = on_error
        self.__on_cancel = on_cancel

    def updated(self, obj: T) -> None:
        self.__on_update(obj)

    def subscription_error(self, error: Exception) -> None:
        if self.__on_error:
            self.__on_error(error)

    def subscription_cancelled(self) -> None:
        if self.__on_cancel:
            self.__on_cancel()
