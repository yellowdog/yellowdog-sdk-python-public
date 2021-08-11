import math
import os
from typing import Optional

from yellowdog_client.model import ObjectUploadRequest
from yellowdog_client.model.exceptions import ErrorType
from yellowdog_client.object_store.abstracts import AbstractObjectStoreServiceProxy as Proxy
from yellowdog_client.object_store.abstracts import AbstractNotificationDispatcher as NotificationDispatcher
from yellowdog_client.object_store.abstracts import AbstractSession
from yellowdog_client.object_store.model import TransferProperties
from yellowdog_client.object_store.model import FileTransferException
from yellowdog_client.object_store.utils import BackgroundThreadFactory as ThreadFactory
from yellowdog_client.object_store.utils import MemoryMappedFileReaderFactory as FileReaderFactory
from yellowdog_client.object_store.utils import ChunkTransferThrottle as ChunkThrottle
from yellowdog_client.object_store.utils import HashUtils
from yellowdog_client.object_store import ServiceSessionFacade
from .upload_session import UploadSession
from .chunk_upload_task import ChunkUploadTask
from .abstracts import AbstractUploadBatchBuilder
from .abstracts import AbstractUploadEngine
from .upload_batch_builder import UploadBatchBuilder


class UploadEngine(AbstractUploadEngine):
    def __init__(self, service_proxy, thread_factory, file_reader_factory, notification_dispatcher,
                 chunk_transfer_throttle, upload_thread_count):
        # type: (Proxy, ThreadFactory, FileReaderFactory, NotificationDispatcher, ChunkThrottle, int) -> None
        super(UploadEngine, self).__init__(
            service_proxy=service_proxy,
            thread_factory=thread_factory,
            notification_dispatcher=notification_dispatcher,
            chunk_transfer_throttle=chunk_transfer_throttle,
            transfer_thread_count=upload_thread_count
        )
        self._file_reader_factory = file_reader_factory  # type: FileReaderFactory

    def _transfer_chunk(self, chunk_transfer_task, chunk_hash):  # NOSONAR chunk_hash used for download
        # type: (ChunkUploadTask, str) -> str
        chunk_data = chunk_transfer_task.read_chunk_data()
        if chunk_data is None or len(chunk_data) == 0:
            raise FileTransferException(ErrorType.ChunkTransferException, "Reader returned no chunk data")

        chunk_hash = HashUtils.calculate_md5_in_base_64(input_value=chunk_data)

        self._service_proxy.upload_chunk(
            session_id=chunk_transfer_task.session_id,
            chunk_number=chunk_transfer_task.chunk_number,
            chunk_data=chunk_data,
            chunk_hash=chunk_hash
        )
        return chunk_hash

    def build_upload_batch(self) -> AbstractUploadBatchBuilder:
        return UploadBatchBuilder(upload_engine=self)

    @staticmethod
    def _create_upload_request(file_path: str, destination_file_name: str, chunk_size: int) -> ObjectUploadRequest:
        file_length = os.path.getsize(file_path)
        chunk_count = int(math.floor(file_length / chunk_size))

        if file_length % chunk_size > 0:
            chunk_count += 1

        return ObjectUploadRequest(
            objectName=destination_file_name,
            objectSize=file_length,
            chunkSize=chunk_size,
            chunkCount=chunk_count
        )

    def create_upload_session(self, file_namespace, source_file_path, destination_file_name, transfer_properties=None):
        # type: (str, str, str, Optional[TransferProperties]) -> AbstractSession
        if transfer_properties is None:
            transfer_properties = TransferProperties()
            transfer_properties.chunk_size = self._chunk_size
            transfer_properties.file_max_attempts = self._file_retry_count

        upload_request = self._create_upload_request(
            file_path=source_file_path,
            destination_file_name=destination_file_name,
            chunk_size=transfer_properties.chunk_size
        )
        session_id = self._service_proxy.start_upload_session(
            namespace=file_namespace,
            object_upload_request=upload_request
        )
        session_facade = ServiceSessionFacade()
        session_facade.session_id = session_id
        session_facade.upload_engine = self
        session_facade.object_store_service_proxy = self._service_proxy
        session_facade.thread_factory = self._thread_factory
        session_facade.notification_dispatcher = self._notification_dispatcher

        session = UploadSession(
            file_reader_factory=self._file_reader_factory,
            service_session_facade=session_facade,
            file_path=source_file_path,
            file_size=upload_request.objectSize,
            chunk_size=upload_request.chunkSize,
            chunk_count=upload_request.chunkCount,
            file_retry_count=transfer_properties.file_max_attempts
        )

        self._add_session(session=session)

        return session
