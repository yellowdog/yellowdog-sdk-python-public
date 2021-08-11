from enum import Enum


class EventSourceState(Enum):
    CONNECTING = "CONNECTING"
    OPEN = "OPEN"
    CLOSED = "CLOSED"
