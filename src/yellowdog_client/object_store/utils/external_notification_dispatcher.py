from typing import Callable, Any

from yellowdog_client.object_store.abstracts import AbstractNotificationDispatcher


class ExternalNotificationDispatcher(AbstractNotificationDispatcher):
    def __init__(self, dispatch_method: Callable[[Callable], None]) -> None:
        self._dispatch_method: Callable[[Callable], None] = dispatch_method

    def _dispatch_without_exceptions(self, event_handler: Callable, event_args: Any) -> Callable:
        return lambda: self._dispatch_without_exceptions_callback(event_handler=event_handler, event_args=event_args)

    @staticmethod
    def _dispatch_without_exceptions_callback(event_handler: Callable, event_args: Any) -> None:
        try:
            event_handler(event_args)
        except Exception as ex:
            # Ignore exceptions, since they are managed by 3rd party
            print("Exception occurred while dispatching notification. %s" % str(ex))

    def dispatch(self, event_handler: Callable, event_args: Any) -> None:
        if event_handler:
            self._dispatch_method(
                self._dispatch_without_exceptions(
                    event_handler=event_handler,
                    event_args=event_args
                )
            )
