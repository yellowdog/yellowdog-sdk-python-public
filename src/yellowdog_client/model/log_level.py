from enum import Enum


class LogLevel(Enum):
    ERROR = "ERROR"
    WARN = "WARN"
    INFO = "INFO"
    DEBUG = "DEBUG"
    TRACE = "TRACE"

    def __str__(self) -> str:
        return self.name
