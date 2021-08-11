from typing import List

from sseclient import SSEClient, Event
from cancel_token import CancellationToken


class ServerResponse(object):
    __sse_session: SSEClient = None

    def __init__(self, sse_session: SSEClient) -> None:
        self.__sse_session = sse_session

    def yield_session_events(self, cancel_token: CancellationToken) -> List[Event]:
        for event in self.__sse_session:
            is_cancelled = cancel_token.cancelled
            if not is_cancelled:
                yield event
            else:
                return
