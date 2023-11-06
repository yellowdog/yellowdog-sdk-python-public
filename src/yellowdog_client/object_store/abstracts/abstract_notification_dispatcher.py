from typing import Callable

from yellowdog_client.object_store.model import FileTransferEventArgs


class AbstractNotificationDispatcher(object):
    def dispatch(self, event_handler: Callable, event_args: FileTransferEventArgs) -> None:
        raise NotImplementedError("Needs implementation")
