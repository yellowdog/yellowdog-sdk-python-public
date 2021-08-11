from typing import Callable, Any

from cancel_token import CancellationToken

from yellowdog_client.common.server_sent_events.sse4python import ChainedThread
from yellowdog_client.common.server_sent_events.sse4python import ServerSentEvent
from yellowdog_client.common.server_sent_events.sse4python import EventSourceState


class AbstractConnectionState(object):
    state = None                # type: EventSourceState

    def run(self, message_received, error_handle, completed, cancel_token, continuation_callback):
        # type: (Callable[[ServerSentEvent], Any], Callable[[Exception], Any], Callable[[], Any], CancellationToken, Callable[[AbstractConnectionState], None]) -> ChainedThread
        raise NotImplementedError("Needs implementation")
