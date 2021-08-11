from typing import Callable, Any

from cancel_token import CancellationToken

from .chained_thread import ChainedThread
from .server_response import ServerResponse
from .server_sent_event import ServerSentEvent
from .abstracts import AbstractConnectionState
from .web_request_factory import WebRequestFactory


class ConnectingState(AbstractConnectionState):
    def __init__(self, url, web_requester_factory):
        # type: (str, WebRequestFactory) -> None
        if url is None:
            raise ValueError("Url cant be null")
        self.__m_url = url
        if web_requester_factory is None:
            raise ValueError("Factory cant be null")
        self.__m_web_requester_factory = web_requester_factory

    def run(self, message_received, error_handle, completed, cancel_token, continuation_callback):
        # type: (Callable[[ServerSentEvent], Any], Callable[[Exception], Any], Callable[[], Any], CancellationToken, Callable[[AbstractConnectionState], None]) -> ChainedThread
        requester = self.__m_web_requester_factory.create()
        thread = requester.get(
            url=self.__m_url,
            callback=lambda response: self.__resolve_server_response(
                server_response=response,
                cancel_token=cancel_token,
                continuation_callback=continuation_callback
            )
        )
        return thread

    def __resolve_server_response(self, server_response, cancel_token, continuation_callback):
        # type: (ServerResponse, CancellationToken, Callable[[AbstractConnectionState], None]) -> ChainedThread
        if not cancel_token.cancelled:
            from .connected_state import ConnectedState
            thread = ChainedThread(
                callback=continuation_callback,
                target=lambda: ConnectedState(
                    url=self.__m_url,
                    response=server_response,
                    web_requester_factory=self.__m_web_requester_factory
                )
            )
            thread.start()
        else:
            from .disconnected_state import DisconnectedState
            thread = ChainedThread(
                callback=continuation_callback,
                target=lambda: DisconnectedState(
                    url=self.__m_url,
                    web_requester_factory=self.__m_web_requester_factory
                )
            )
            thread.start()
        return thread
