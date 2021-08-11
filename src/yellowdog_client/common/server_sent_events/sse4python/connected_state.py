from typing import Callable, Any

from cancel_token import CancellationToken
from sseclient import Event

from .chained_thread import ChainedThread
from .abstracts import AbstractConnectionState
from .web_request_factory import WebRequestFactory
from .server_response import ServerResponse
from .server_sent_event import ServerSentEvent


class ConnectedState(AbstractConnectionState):
    __m_url = None  # type: str
    __m_response = None                 # type: ServerResponse
    __m_web_requester_factory = None      # type: WebRequestFactory

    def __init__(self, url, response, web_requester_factory):
        # type: (str, ServerResponse, WebRequestFactory) -> None
        self.__m_url = url
        self.__m_response = response
        self.__m_web_requester_factory = web_requester_factory

    def run(self, message_received, error_handle, completed, cancel_token, continuation_callback):
        # type: (Callable[[ServerSentEvent], Any], Callable[[Exception], Any], Callable[[], Any], CancellationToken, Callable[[AbstractConnectionState], None]) -> ChainedThread
        thread = ChainedThread(
            callback=continuation_callback,
            target=lambda: self.__run(
                message_received=message_received,
                error_handle=error_handle,
                completed=completed,
                cancel_token=cancel_token
            )
        )
        thread.start()
        return thread

    def __run(self, message_received, error_handle, completed, cancel_token):
        # type: (Callable[[ServerSentEvent], None], Callable[[Exception], None], Callable[[], None], CancellationToken) -> AbstractConnectionState
        try:
            if not cancel_token.cancelled:
                for event in self.__m_response.yield_session_events(cancel_token=cancel_token):
                    if event:
                        self.__send_event(event, message_received)
        except Exception as ex:
            error_handle(ex)
        completed()
        from .disconnected_state import DisconnectedState
        return DisconnectedState(
            url=self.__m_url,
            web_requester_factory=self.__m_web_requester_factory
        )

    @staticmethod
    def __send_event(sse_event, message_received):
        # type: (Event, Callable[[ServerSentEvent], None]) -> None
        sse_response = ServerSentEvent()
        data = getattr(sse_event, "data", None)
        event_type = getattr(sse_event, "event", None)
        last_event_id = getattr(sse_event, "id", None)
        retry = getattr(sse_event, "retry", None)
        if data:
            sse_response.raw_data = data
        if event_type:
            sse_response.event_type = event_type
        if last_event_id:
            sse_response.last_event_id = last_event_id
        if retry:
            sse_response.retry = int(retry)
        message_received(sse_response)
