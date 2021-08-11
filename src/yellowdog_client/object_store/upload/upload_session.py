from yellowdog_client.object_store.abstracts import AbstractSession
from yellowdog_client.object_store.model import FileTransferDirection
from yellowdog_client.object_store.utils import MemoryMappedFileReaderFactory
from yellowdog_client.object_store.utils import MemoryMappedFileReader
from yellowdog_client.object_store import ServiceSessionFacade
from .chunk_upload_task import ChunkUploadTask


class UploadSession(AbstractSession):
    """
    Transfer session used for upload

    .. versionadded:: 0.5.0

    .. seealso::

        Inherits from :class:`yellowdog_client.object_store.abstracts.AbstractSession`
    """

    _chunk_task_type = ChunkUploadTask                          # type: type
    _file_io = None                                             # type: MemoryMappedFileReader

    def __init__(self, file_reader_factory, service_session_facade, file_path, file_size,       # NOSONAR
                 chunk_size, chunk_count, file_retry_count):
        # type: (MemoryMappedFileReaderFactory, ServiceSessionFacade, str, int, int, int, int) -> None
        super(UploadSession, self).__init__(
            direction=FileTransferDirection.Upload,
            service_session_facade=service_session_facade,
            file_path=file_path,
            file_size=file_size,
            chunk_size=chunk_size,
            chunk_count=chunk_count,
            file_retry_count=file_retry_count
        )
        self._file_reader_factory = file_reader_factory         # type: MemoryMappedFileReaderFactory

    def _on_build_chunk_transfer_task(self, task):
        # type: (ChunkUploadTask) -> None
        task.read_chunk_data = lambda: self._file_io.read_bytes(
            offset=self._calculate_chunk_offset(chunk_number=task.chunk_number),
            size=task.chunk_size
        )

    def _start_transfer(self):
        # type: () -> None
        file_reader = self._file_reader_factory.new_reader(file_path=self.file_path)
        self._start_transfer_session(
            file_io=file_reader,
            enqueue_chunk_task_method=self._service_session_facade.enqueue_chunk_upload
        )
