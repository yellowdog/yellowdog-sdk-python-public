import os

from yellowdog_client.object_store.abstracts import AbstractSession
from yellowdog_client.object_store.model import FileTransferDirection
from yellowdog_client.object_store import ServiceSessionFacade
from yellowdog_client.object_store.utils import MemoryMappedFileWriterFactory
from yellowdog_client.object_store.utils import MemoryMappedFileWriter
from yellowdog_client.object_store.utils import FileUtils
from .chunk_download_task import ChunkDownloadTask


class DownloadSession(AbstractSession):
    """
    Transfer session used for download

    .. versionadded:: 0.5.0

    .. seealso::

        Inherits from :class:`yellowdog_client.object_store.abstracts.AbstractSession`
    """

    _chunk_task_type: type = ChunkDownloadTask
    _file_io: MemoryMappedFileWriter = None
    ON_PROGRESS_EXTENSION: str = ".inprogress"

    def __init__(
            self,
            file_reader_factory: MemoryMappedFileWriterFactory,
            service_session_facade: ServiceSessionFacade,
            file_path: str,
            file_size: int,
            chunk_size: int,
            chunk_count: int,
            file_retry_count: int
    ) -> None:
        super(DownloadSession, self).__init__(
            direction=FileTransferDirection.Download,
            service_session_facade=service_session_facade,
            file_path=file_path,
            file_size=file_size,
            chunk_size=chunk_size,
            chunk_count=chunk_count,
            file_retry_count=file_retry_count
        )
        self._file_writer_factory: MemoryMappedFileWriterFactory = file_reader_factory
        self._file_path_in_progress: str = "%s%s" % (file_path, self.ON_PROGRESS_EXTENSION)

    def _on_build_chunk_transfer_task(self, task: ChunkDownloadTask) -> None:
        task.write_chunk_data = lambda chunk_data: self._file_io.write_bytes(
            offset=self._calculate_chunk_offset(chunk_number=task.chunk_number),
            str_bytes=chunk_data
        )

    def _on_complete(self) -> None:
        FileUtils.rename_replace(self._file_path_in_progress, self.file_path)

    def _on_abort(self) -> None:
        FileUtils.with_retry(action=lambda: os.remove(self._file_path_in_progress))

    def _start_transfer(self) -> None:
        if self.file_size != 0:
            file_writer = self._file_writer_factory.new_writer(
                file_path=self._file_path_in_progress,
                file_size=self.file_size
            )
            self._start_transfer_session(
                file_io=file_writer,
                enqueue_chunk_task_method=self._service_session_facade.enqueue_chunk_download
            )
        else:
            directory_path = os.path.dirname(self._file_path_in_progress)
            if not os.path.isdir(directory_path):
                os.makedirs(directory_path)
            open(self._file_path_in_progress, "w+b").close()
            self._complete()
