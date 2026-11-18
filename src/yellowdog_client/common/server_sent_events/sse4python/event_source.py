from threading import Lock, Thread
from typing import Callable, Dict, List, Optional, Tuple, TypeVar

from requests.auth import AuthBase

from yellowdog_client.common import CancellationToken
from .event_source_state import EventSourceState
from .server_sent_event import ServerSentEvent
from .sse_stream import RequestsSseClient

L = TypeVar('L')


class EventSource:
    def __init__(
            self,
            url: str,
            auth: AuthBase,
            headers: Dict[str, str],
            timeout: Tuple[Optional[float], Optional[float]] = (None, None)
    ) -> None:
        self.__url: str = url
        self.__auth: AuthBase = auth
        self.__headers: Dict[str, str] = headers
        self.__timeout: Tuple[Optional[float], Optional[float]] = timeout
        self._token_source: CancellationToken = CancellationToken()
        self._current_state: EventSourceState = EventSourceState.CLOSED
        self._listeners_lock = Lock()
        self._event_received_listeners: List[Callable[[ServerSentEvent], None]] = []
        self._error_received_listeners: List[Callable[[Exception], None]] = []
        self._event_source_completed_listeners: List[Callable[[], None]] = []

    def add_event_received_listener(self, listener: Callable[[ServerSentEvent], None]) -> None:
        with self._listeners_lock:
            self._event_received_listeners.append(listener)

    def add_error_received_listener(self, listener: Callable[[Exception], None]) -> None:
        with self._listeners_lock:
            self._error_received_listeners.append(listener)

    def add_event_source_completed_listener(self, listener: Callable[[], None]) -> None:
        with self._listeners_lock:
            self._event_source_completed_listeners.append(listener)

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
            stream = RequestsSseClient(self.__url, self.__auth, self.__headers, timeout=self.__timeout).stream()
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
        return self._dispatch(self._error_received_listeners, lambda listener: listener(ex))

    def _on_event_source_completed(self) -> Thread:
        if not self._token_source.cancelled:
            self._token_source.cancel()
        return self._dispatch(self._event_source_completed_listeners, lambda listener: listener())

    def _on_event_received(self, sse: ServerSentEvent) -> Thread:
        return self._dispatch(self._event_received_listeners, lambda listener: listener(sse))

    def _dispatch(self, listeners: List[L], notify: Callable[[L], None]) -> Thread:
        with self._listeners_lock:
            listeners_to_notify = list(listeners)

        def notify_all() -> None:
            for listener in listeners_to_notify:
                notify(listener)

        thread = Thread(target=notify_all)
        thread.start()
        return thread
