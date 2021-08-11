import traceback


class Closeable(object):
    def __enter__(self):
        # type: () -> Closeable
        return self

    def __exit__(self, exception_type, exception_value, exception_traceback):
        # type: (type, Exception, traceback) -> None
        self.close()

    def close(self):
        # type: () -> None
        raise NotImplementedError("Needs implementation")
