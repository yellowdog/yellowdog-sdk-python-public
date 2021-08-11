from typing import Callable, Any

from cancel_token import CancellationToken

from .chained_thread import ChainedThread
from .server_sent_event import ServerSentEvent
from .abstracts import AbstractConnectionState
from .web_request_factory import WebRequestFactory
from .event_source_state import EventSourceState


class DisconnectedState(AbstractConnectionState):
    __m_url = None  # type: str
    __m_web_requester_factory = None  # type: WebRequestFactory
    state = EventSourceState.CLOSED

    def __init__(self, url, web_requester_factory):
        # type: (str, WebRequestFactory) -> None
        if url is None:
            raise ValueError("Url cant be null")
        self.__m_url = url
        self.__m_web_requester_factory = web_requester_factory

    def run(self, message_received, error_handle, completed, cancel_token, continuation_callback):
        # type: (Callable[[ServerSentEvent], Any], Callable[[Exception], Any], Callable[[], Any], CancellationToken, Callable[[AbstractConnectionState], None]) -> ChainedThread
        if cancel_token.cancelled:
            thread = ChainedThread(
                callback=continuation_callback,
                target=lambda: DisconnectedState(
                    url=self.__m_url,
                    web_requester_factory=self.__m_web_requester_factory
                )
            )
            thread.start()
        else:
            from .connecting_state import ConnectingState
            thread = ChainedThread(
                callback=continuation_callback,
                target=lambda: ConnectingState(
                    url=self.__m_url,
                    web_requester_factory=self.__m_web_requester_factory
                )
            )
            thread.start()
        return thread
