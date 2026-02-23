from types import TracebackType
from typing import Type, Any


class Closeable(object):
    def __enter__(self) -> 'Closeable':
        return self

    def __exit__(self, exception_type: Type[Any], exception_value: Exception, exception_traceback: TracebackType) -> None:
        self.close()

    def close(self) -> None:
        raise NotImplementedError("Needs implementation")
