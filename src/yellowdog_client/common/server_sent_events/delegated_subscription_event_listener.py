from typing import Callable, TypeVar

from .subscription_event_listener import SubscriptionEventListener

T = TypeVar('T')


class DelegatedSubscriptionEventListener(SubscriptionEventListener):
    """
    Simple callback listener

    Constructor accepts the following **arguments**:

    :param on_update: mandatory. Callback for object updates
    :type on_update: Callable[[TypeVar], None]
    :param on_error: optional. Callback for exceptions, received from the ``server sent events``
    :type on_error: Callable[[:class:`Exception`], None]
    :param on_cancel: optional. Callback for listener cancellation events
    :type on_cancel: Callable[[], None]
    """

    __on_update = None  # type: Callable[[T], None]
    __on_error = None  # type: Callable[[Exception], None]
    __on_cancel = None              # type: Callable[[], None]

    def __init__(self, on_update, on_error, on_cancel):
        # type: (Callable[[T], None], Callable[[Exception], None], Callable[[], None]) -> None
        self.__on_update = on_update
        self.__on_error = on_error
        self.__on_cancel = on_cancel

    def updated(self, obj):
        # type: (T) -> None
        self.__on_update(obj)

    def subscription_error(self, error):
        # type: (Exception) -> None
        self.__on_error(error)

    def subscription_cancelled(self):
        # type: () -> None
        self.__on_cancel()
