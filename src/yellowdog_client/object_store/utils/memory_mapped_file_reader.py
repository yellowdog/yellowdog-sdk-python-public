from mmap import mmap as memory_map
import mmap

from yellowdog_client.common import Closeable


class MemoryMappedFileReader(Closeable):
    def __init__(self, file_path):
        # type: (str) -> None
        self._opened_file = open(file_path, "r")
        self._memory_file = memory_map(fileno=self._opened_file.fileno(), length=0, offset=0, access=mmap.ACCESS_READ)

    def read_bytes(self, offset, size):
        # type: (int, int) -> str
        self._memory_file.seek(offset)
        res = self._memory_file.read(size)
        return res

    def close(self):
        # type: () -> None
        self._memory_file.close()
        self._opened_file.close()
