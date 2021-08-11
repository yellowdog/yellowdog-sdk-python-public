from typing import Callable

from yellowdog_client.object_store.model import FileTransferEventArgs


class AbstractNotificationDispatcher(object):
    def dispatch(self, event_handler, event_args):
        # type: (Callable, FileTransferEventArgs) -> None
        raise NotImplementedError("Needs implementation")
