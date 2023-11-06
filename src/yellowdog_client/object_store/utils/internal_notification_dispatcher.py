from queue import Queue
from typing import Callable, Any

from cancel_token import CancellationToken

from yellowdog_client.object_store.utils.background_thread_factory import BackgroundThreadFactory
from yellowdog_client.object_store.abstracts import AbstractNotificationDispatcher


class InternalNotificationDispatcher(AbstractNotificationDispatcher):
    def __init__(self, thread_factory: BackgroundThreadFactory) -> None:
        self._action_queue: Queue = Queue()
        self.cancellation_token: CancellationToken = CancellationToken()
        self.background_thread = thread_factory.new_thread(target=self.dispatch_notifications)
        self.background_thread.start()

    def dispatch_notifications(self) -> None:
        while not self.cancellation_token.cancelled:
            try:
                action = self._action_queue.get()
                action()
            except Exception as ex:
                print("Failed to dispatch message. %s" % str(ex))

    def dispatch(self, event_handler: Callable, event_args: Any) -> None:
        if event_handler:
            self._action_queue.put(item=lambda: event_handler(event_args))
