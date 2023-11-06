from threading import Thread
from threading import Thread
from typing import Callable

from cancel_token import CancellationToken
from pydispatch import Dispatcher
from requests.auth import AuthBase

from .event_source_state import EventSourceState
from .server_sent_event import ServerSentEvent
from .sse_stream import RequestsSseClient


class EventSource(Dispatcher):
    EVENT_SOURCE_COMPLETED = "event_source_completed"
    EVENT_RECEIVED = "event_received"
    ERROR_RECEIVED = "error_received"
    _events_ = [EVENT_SOURCE_COMPLETED, EVENT_RECEIVED, ERROR_RECEIVED]

    def __init__(self, url: str, auth: AuthBase) -> None:
        super(EventSource, self).__init__(None, None)
        self.__url: str = url
        self.__auth: AuthBase = auth
        self._token_source: CancellationToken = CancellationToken()
        self._current_state: EventSourceState = EventSourceState.CLOSED

    @property
    def is_closed(self) -> bool:
        return self._token_source.cancelled and self.state == EventSourceState.CLOSED

    @property
    def state(self) -> EventSourceState:
        return self._current_state

    def start(self) -> None:
        if self.state == EventSourceState.CLOSED:
            self._token_source = CancellationToken()
            Thread(target=self._run, daemon=True).start()

    def stop(self) -> None:
        if not self._token_source.cancelled:
            self._token_source.cancel()
            self._on_event_source_completed()

    def _run(self) -> None:
        try:
            self._current_state = EventSourceState.CONNECTING
            stream = RequestsSseClient(self.__url, self.__auth).stream()
        except Exception as ex:
            self._on_error_received(ex)
            self._current_state = EventSourceState.CLOSED
            return

        self._current_state = EventSourceState.OPEN

        try:
            for event in stream:
                if self._token_source.cancelled:
                    break
                if event:
                    self._on_event_received(event)
        except Exception as ex:
            self._on_error_received(ex)
        finally:
            self._current_state = EventSourceState.CLOSED
            self._on_event_source_completed()

    def _on_error_received(self, ex: Exception) -> Thread:
        return self._dispatch(lambda: self.emit(name=self.ERROR_RECEIVED, error=ex))

    def _on_event_source_completed(self) -> Thread:
        if not self._token_source.cancelled:
            self._token_source.cancel()
        return self._dispatch(lambda: self.emit(name=self.EVENT_SOURCE_COMPLETED))

    def _on_event_received(self, sse: ServerSentEvent) -> Thread:
        return self._dispatch(lambda: self.emit(name=self.EVENT_RECEIVED, message=sse))

    @staticmethod
    def _dispatch(callback: Callable) -> Thread:
        thread = Thread(target=callback)
        thread.start()
        return thread
