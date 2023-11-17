from mmap import mmap as memory_map
import mmap

from yellowdog_client.common import Closeable


class MemoryMappedFileReader(Closeable):
    def __init__(self, file_path: str) -> None:
        self._opened_file = open(file_path, "r")

        try:
            self._memory_file = memory_map(
                fileno=self._opened_file.fileno(),
                length=0,
                offset=0,
                access=mmap.ACCESS_READ
            )
        except ValueError as ex:
            if str(ex) == "cannot mmap an empty file":
                self._memory_file = self._opened_file

    def read_bytes(self, offset: int, size: int) -> str:
        self._memory_file.seek(offset)
        res = self._memory_file.read(size)
        return res

    def close(self) -> None:
        self._memory_file.close()
        self._opened_file.close()
