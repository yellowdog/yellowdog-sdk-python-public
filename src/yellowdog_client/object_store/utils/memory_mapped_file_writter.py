import os
from mmap import mmap as memory_map
from threading import Lock

from yellowdog_client.common import Closeable


class MemoryMappedFileWriter(Closeable):
    def __init__(self, file_path: str, file_size: int) -> None:
        directory_path = os.path.dirname(file_path)
        if not os.path.isdir(directory_path):
            os.makedirs(directory_path)
        self._file_size = file_size

        # On Ubuntu OS first need to allocate correct size file before memory-mapping
        with open(file_path, "w+b") as f:
            f.seek(self._file_size - 1)
            f.write(b"\0")

        # Start memory mapping
        self._created_file = open(file_path, "a+b")
        self._memory_file = memory_map(
            fileno=self._created_file.fileno(),
            length=0
        )
        self._write_lock = Lock()

    def write_bytes(self, offset: int, str_bytes: str) -> None:
        """this method must be thread safe"""
        if not isinstance(str_bytes, bytes):
            str_bytes = str_bytes.encode('utf-8')
        with self._write_lock:
            self._memory_file.seek(offset)
            self._memory_file.write(str_bytes)
            self._memory_file.flush(offset, len(str_bytes))

    def close(self) -> None:
        self._memory_file.close()
        self._created_file.close()
