import traceback
from typing import Type


class Closeable(object):
    def __enter__(self) -> 'Closeable':
        return self

    def __exit__(self, exception_type: Type, exception_value: Exception, exception_traceback: traceback) -> None:
        self.close()

    def close(self) -> None:
        raise NotImplementedError("Needs implementation")
