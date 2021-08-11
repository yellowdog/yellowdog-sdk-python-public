from typing import Callable
from threading import Thread

from cancel_token import CancellationToken
from pydispatch import Dispatcher

from .web_request_factory import WebRequestFactory
from .event_source_state import EventSourceState
from .disconnected_state import DisconnectedState
from .server_sent_event import ServerSentEvent
from .abstracts import AbstractConnectionState


class EventSource(Dispatcher):
    EVENT_SOURCE_COMPLETED = "event_source_completed"
    EVENT_RECEIVED = "event_received"
    STATE_CHANGED = "state_changed"
    ERROR_RECEIVED = "error_received"
    _events_ = [EVENT_SOURCE_COMPLETED, EVENT_RECEIVED, STATE_CHANGED, ERROR_RECEIVED]

    __url = None                            # type: str
    __web_requester_factory = None          # type: WebRequestFactory
    _token_source = None                   # type: CancellationToken
    _current_state_internal = None         # type: AbstractConnectionState

    def __init__(self, url, factory):
        # type: (str, WebRequestFactory) -> None
        super(EventSource, self).__init__(None, None)
        self.__url = url
        self.__web_requester_factory = factory
        self._token_source = CancellationToken()
        self._current_state = DisconnectedState(url=self.__url, web_requester_factory=self.__web_requester_factory)

    @property
    def is_closed(self):
        # type: () -> bool
        return self._token_source.cancelled and self.state == EventSourceState.CLOSED

    @property
    def state(self):
        # type: () -> EventSourceState
        return self._current_state.state

    @property
    def _current_state(self):
        # type: () -> AbstractConnectionState
        return self._current_state_internal

    @_current_state.setter
    def _current_state(self, value):
        # type: (AbstractConnectionState) -> None
        if self._current_state_internal == value:
            return
        self._current_state_internal = value
        self._on_status_changed(state=self._current_state_internal.state)

    def start(self):
        # type: () -> None
        if self.state == EventSourceState.CLOSED:
            self._token_source = CancellationToken()
            self._run()

    def stop(self):
        # type: () -> None
        if not self._token_source.cancelled:
            self._token_source.cancel()
            self._on_event_source_completed()

    def _run(self):
        # type: () -> None
        if self._token_source.cancelled and self._current_state.state == EventSourceState.CLOSED:
            return

        self._current_state.run(
            message_received=self._on_event_received,
            error_handle=self._on_error_received,
            completed=self._on_event_source_completed,
            cancel_token=self._token_source,
            continuation_callback=self._continuation_callback
        )

    def _continuation_callback(self, connection_state):
        # type: (AbstractConnectionState) -> None
        self._current_state = connection_state
        self._run()

    def _on_error_received(self, ex):
        # type: (Exception) -> Thread
        return self._dispatch(lambda: self.emit(name=self.ERROR_RECEIVED, error=ex))

    def _on_event_source_completed(self):
        # type: () -> Thread
        if not self._token_source.cancelled:
            self._token_source.cancel()
        return self._dispatch(lambda: self.emit(name=self.EVENT_SOURCE_COMPLETED))

    def _on_event_received(self, sse):
        # type: (ServerSentEvent) -> Thread
        return self._dispatch(lambda: self.emit(name=self.EVENT_RECEIVED, message=sse))

    def _on_status_changed(self, state):
        # type: (EventSourceState) -> Thread
        return self._dispatch(lambda: self.emit(name=self.STATE_CHANGED, state=state))

    @staticmethod
    def _dispatch(callback):
        # type: (Callable) -> Thread
        thread = Thread(target=callback)
        thread.start()
        return thread

