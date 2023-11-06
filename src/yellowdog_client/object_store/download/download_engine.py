from typing import Optional
import os

from .abstracts import AbstractDownloadEngine
from .abstracts import AbstractDownloadBatchBuilder
from .download_session import DownloadSession
from .download_batch_builder import DownloadBatchBuilder
from .chunk_download_task import ChunkDownloadTask
from yellowdog_client.model import ObjectDownloadRequest
from yellowdog_client.model.exceptions import ErrorType
from yellowdog_client.object_store import ServiceSessionFacade
from yellowdog_client.object_store.model import TransferProperties
from yellowdog_client.object_store.model import FileTransferException
from yellowdog_client.object_store.abstracts import AbstractObjectStoreServiceProxy as Proxy
from yellowdog_client.object_store.abstracts import AbstractSession
from yellowdog_client.object_store.utils import BackgroundThreadFactory as ThreadFactory
from yellowdog_client.object_store.utils import MemoryMappedFileWriterFactory as WriterFactory
from yellowdog_client.object_store.utils import ChunkTransferThrottle as ChunkThrottle
from yellowdog_client.object_store.utils import HashUtils
from yellowdog_client.object_store.abstracts import AbstractNotificationDispatcher as NotificationDispatcher


class DownloadEngine(AbstractDownloadEngine):
    def __init__(
            self,
            service_proxy: Proxy,
            thread_factory: ThreadFactory,
            file_writer_factory: WriterFactory,
            notification_dispatcher: NotificationDispatcher,
            chunk_transfer_throttle: ChunkThrottle,
            download_thread_count: int
    ) -> None:
        super(DownloadEngine, self).__init__(
            service_proxy=service_proxy,
            thread_factory=thread_factory,
            notification_dispatcher=notification_dispatcher,
            chunk_transfer_throttle=chunk_transfer_throttle,
            transfer_thread_count=download_thread_count
        )
        self._file_writer_factory: WriterFactory = file_writer_factory

    def _transfer_chunk(self, chunk_transfer_task: ChunkDownloadTask, chunk_hash: str) -> str:
        chunk_data, chunk_hash = self._service_proxy.download_chunk(
            session_id=chunk_transfer_task.session_id,
            chunk_number=chunk_transfer_task.chunk_number,
            chunk_size=chunk_transfer_task.chunk_size,
            chunk_hash=chunk_hash
        )

        if chunk_data is None or len(chunk_data) == 0:
            raise FileTransferException(
                ErrorType.ChunkTransferException,
                "Server returned no chunk data"
            )

        if HashUtils.calculate_md5_in_base_64(input_value=chunk_data) != chunk_hash:
            raise FileTransferException(
                ErrorType.ChunkTransferException,
                "Chunk hash returned by service does not match calculated"
            )

        chunk_transfer_task.write_chunk_data(chunk_data)

        return chunk_hash

    def build_download_batch(self) -> AbstractDownloadBatchBuilder:
        return DownloadBatchBuilder(download_engine=self, service_proxy=self._service_proxy)

    def create_download_session(self, file_namespace: str, file_name: str, destination_folder_path: str,
                                destination_file_name: Optional[str] = None,
                                transfer_properties: Optional[TransferProperties] = None) -> AbstractSession:
        if destination_file_name is None:
            destination_file_name = file_name
        if transfer_properties is None:
            transfer_properties = TransferProperties()
            transfer_properties.chunk_size = self.chunk_size
            transfer_properties.file_max_attempts = self.file_retry_count

        full_path = os.path.join(destination_folder_path, destination_file_name)

        download_request = ObjectDownloadRequest(objectName=file_name, chunkSize=transfer_properties.chunk_size)

        download_response = self._service_proxy.start_download_session(
            namespace=file_namespace,
            object_download_request=download_request
        )

        session_facade = ServiceSessionFacade()
        session_facade.session_id = download_response.sessionId
        session_facade.download_engine = self
        session_facade.object_store_service_proxy = self._service_proxy
        session_facade.thread_factory = self._thread_factory
        session_facade.notification_dispatcher = self._notification_dispatcher

        session = DownloadSession(
            file_reader_factory=self._file_writer_factory,
            service_session_facade=session_facade,
            file_path=full_path,
            file_size=download_response.objectSize,
            chunk_size=download_response.chunkSize,
            chunk_count=download_response.chunkCount,
            file_retry_count=transfer_properties.file_max_attempts
        )

        self._add_session(session=session)

        return session
