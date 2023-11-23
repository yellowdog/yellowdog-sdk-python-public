import os
from typing import List, Optional, Union

from pydispatch import Dispatcher

from yellowdog_client.model import Slice
from yellowdog_client.model import ObjectDetail, ObjectPath, ObjectPathsRequest, ObjectPathsSliceRequest
from yellowdog_client.common.decorators.dispatcher import dispatch_async
from yellowdog_client.common import Closeable
from yellowdog_client.model import NamespaceStorageConfiguration
from yellowdog_client.object_store.model import TransferProperties
from yellowdog_client.object_store.utils import ActionUtils
from yellowdog_client.object_store.utils import BackgroundThreadFactory
from yellowdog_client.object_store.utils import ChunkTransferThrottle
from yellowdog_client.object_store.utils import InternalNotificationDispatcher
from yellowdog_client.object_store.utils import MemoryMappedFileReaderFactory
from yellowdog_client.object_store.utils import MemoryMappedFileWriterFactory
from .abstracts import AbstractSession
from .download import DownloadEngine
from .download.abstracts import AbstractDownloadBatchBuilder
from .model import ClientErrorEventArgs
from .object_store_service_proxy import ObjectStoreServiceProxy
from .upload import UploadEngine
from .upload.abstracts import AbstractUploadBatchBuilder


class ObjectStoreClient(Closeable, Dispatcher):
    """
    The API interface exposed by the YellowDog `Object Store Service`
    """
    ON_ERROR = "on_error"
    _events_ = [ON_ERROR]
    DEFAULT_UPLOAD_THROTTLE_PERIOD_SEC = 10
    DEFAULT_UPLOAD_THREAD_COUNT = 10
    DEFAULT_UPLOAD_CHUNK_SIZE = 5242880
    DEFAULT_DOWNLOAD_THROTTLE_PERIOD_SEC = 10
    DEFAULT_DOWNLOAD_THREAD_COUNT = 10
    DEFAULT_DOWNLOAD_CHUNK_SIZE = 5242880

    def __init__(self, proxy: ObjectStoreServiceProxy) -> None:
        super(ObjectStoreClient, self).__init__()
        self._service_proxy = proxy
        self._service_proxy.bind(on_error=self._dispatch_error_notification)
        self._notification_dispatcher = InternalNotificationDispatcher(thread_factory=BackgroundThreadFactory())

        self._upload_engine = UploadEngine(
            service_proxy=self._service_proxy,
            thread_factory=BackgroundThreadFactory(),
            file_reader_factory=MemoryMappedFileReaderFactory(),
            notification_dispatcher=InternalNotificationDispatcher(thread_factory=BackgroundThreadFactory()),
            chunk_transfer_throttle=ChunkTransferThrottle(throttle_period_sec=self.DEFAULT_UPLOAD_THROTTLE_PERIOD_SEC),
            upload_thread_count=self.DEFAULT_UPLOAD_THREAD_COUNT
        )
        self._upload_engine.chunk_size = self.DEFAULT_UPLOAD_CHUNK_SIZE

        self._download_engine = DownloadEngine(
            service_proxy=self._service_proxy,
            thread_factory=BackgroundThreadFactory(),
            file_writer_factory=MemoryMappedFileWriterFactory(),
            notification_dispatcher=InternalNotificationDispatcher(thread_factory=BackgroundThreadFactory()),
            chunk_transfer_throttle=ChunkTransferThrottle(
                throttle_period_sec=self.DEFAULT_DOWNLOAD_THROTTLE_PERIOD_SEC),
            download_thread_count=self.DEFAULT_DOWNLOAD_THREAD_COUNT
        )
        self._download_engine.chunk_size = self.DEFAULT_DOWNLOAD_CHUNK_SIZE
        # to detect redundant calls
        self._disposed_value = False

    @property
    def active_sessions(self) -> List[AbstractSession]:
        """
        :getter: List of active sessions for both upload and download
        :rtype: List of :class:`yellowdog_client.object_store.abstracts.AbstractSession`
        """
        return self._upload_engine.active_sessions + self._download_engine.active_sessions

    @property
    def all_sessions(self) -> List[AbstractSession]:
        """
        :getter: List of all sessions (active and inactive) for both upload and download
        :rtype: List of :class:`yellowdog_client.object_store.abstracts.AbstractSession`
        """
        return self._upload_engine.all_sessions + self._download_engine.all_sessions

    @property
    def uploads_active(self) -> bool:
        """
        :getter: True, if any of upload threads are actively transferring chunks
        :rtype: bool
        """
        return self._upload_engine.transfer_threads_alive

    @property
    def downloads_active(self) -> bool:
        """
        :getter: True, if any of download threads are actively transferring chunks
        :rtype: bool
        """
        return self._download_engine.transfer_threads_alive

    @property
    def upload_chunk_size(self) -> int:
        """
        :getter: chunk size in bytes, used for uploads
        :setter: chunk size in bytes for upload to use
        :type: int
        """
        return self._upload_engine.chunk_size

    @upload_chunk_size.setter
    def upload_chunk_size(self, value: int) -> None:
        self._upload_engine.chunk_size = value

    @property
    def download_chunk_size(self) -> int:
        """
        :getter: chunk size in bytes, used for downloads
        :setter: chunk size in bytes for download to use
        :type: int
        """
        return self._download_engine.chunk_size

    @download_chunk_size.setter
    def download_chunk_size(self, value: int) -> None:
        self._download_engine.chunk_size = value

    @property
    def upload_file_retry_count(self) -> int:
        """
        :getter: number of retries, which will be attempted in case of upload failure
        :setter: number of retries for uploads to use
        :type: int
        """
        return self._upload_engine.file_retry_count

    @upload_file_retry_count.setter
    def upload_file_retry_count(self, value: int) -> None:
        self._upload_engine.file_retry_count = value

    @property
    def download_file_retry_count(self) -> int:
        """
        :getter: number of retries, which will be attempted in case of download failure
        :setter: number of retries for downloads to use
        :type: int
        """
        return self._download_engine.file_retry_count

    @download_file_retry_count.setter
    def download_file_retry_count(self, value: int) -> None:
        self._download_engine.file_retry_count = value

    @property
    def upload_max_bytes_per_second(self) -> int:
        """
        :getter: limit of bytes per second allowed for upload. If equal to 0, no throttle is applied
        :setter: sets a number of max bytes per second for upload engine to allow transferring
        :type: int
        """
        return self._upload_engine.max_bytes_per_second

    @upload_max_bytes_per_second.setter
    def upload_max_bytes_per_second(self, value: int) -> None:
        self._upload_engine.max_bytes_per_second = value

    @property
    def download_max_bytes_per_second(self) -> int:
        """
        :getter: limit of bytes per second allowed for download. If equal to 0, no throttle is applied
        :setter: sets a number of max bytes per second for download engine to allow transferring
        :type: int
        """
        return self._download_engine.max_bytes_per_second

    @download_max_bytes_per_second.setter
    def download_max_bytes_per_second(self, value: int) -> None:
        self._download_engine.max_bytes_per_second = value

    def build_upload_batch(self) -> AbstractUploadBatchBuilder:
        """
        Retrieves a batch builder for uploads, which is used to create multiple upload sessions

        :return: upload batch builder
        :rtype: :class:`yellowdog_client.object_store.upload.UploadBatchBuilder`
        """
        return self._upload_engine.build_upload_batch()

    def build_download_batch(self) -> AbstractDownloadBatchBuilder:
        """
        Retrieves a batch builder for downloads, which is used to create multiple download sessions

        :return: download batch builder
        :rtype: :class:`yellowdog_client.object_store.download.DownloadBatchBuilder`
        """
        return self._download_engine.build_download_batch()

    def create_upload_session(self, file_namespace: str, source_file_path: str, destination_file_name: Optional[str] = None,
                              transfer_properties: Optional[TransferProperties] = None) -> AbstractSession:
        """
        Creates a new upload session for the file

        :param file_namespace: Namespace for file storage
        :type file_namespace: str
        :param source_file_path: path of the file to upload
        :type source_file_path: str
        :param destination_file_name: new name of the file to use within object store namespace
        :type destination_file_name: Optional[str]
        :param transfer_properties: custom properties to use for file transfer
        :type transfer_properties: Optional[:class:`yellowdog_client.object_store.model.TransferProperties`]
        :return: upload session, which, upon return, can be started or aborted
        :rtype: :class:`yellowdog_client.object_store.upload.UploadSession`
        """
        if not destination_file_name:
            destination_file_name = os.path.basename(source_file_path)

        return self._upload_engine.create_upload_session(
            file_namespace=file_namespace,
            source_file_path=source_file_path,
            destination_file_name=destination_file_name,
            transfer_properties=transfer_properties
        )

    def create_download_session(self, file_namespace: str, file_name: str, destination_folder_path: str, destination_file_name: Optional[str] = None,
                                transfer_properties: Optional[TransferProperties] = None) -> AbstractSession:
        """
        Creates a new upload session for the file

        :param file_namespace: Namespace for file storage
        :type file_namespace: str
        :param file_name: path of the file to upload
        :type file_name: str
        :param destination_folder_path: directory path to store downloaded file
        :type destination_folder_path: str
        :param destination_file_name: new name of the file to use within object store namespace
        :type destination_file_name: Optional[str]
        :param transfer_properties: custom properties to use for file transfer
        :type transfer_properties: Optional[:class:`yellowdog_client.object_store.model.TransferProperties`]
        :return: upload session, which, upon return, can be started or aborted
        :rtype: :class:`yellowdog_client.object_store.upload.UploadSession`
        """
        return self._download_engine.create_download_session(
            file_namespace=file_namespace,
            file_name=file_name,
            destination_folder_path=destination_folder_path,
            destination_file_name=destination_file_name,
            transfer_properties=transfer_properties
        )

    def start_transfers(self) -> None:
        """
        Enables both uploads and downloads for yellowdog object store. Required to make any transfers using the client
        """
        ActionUtils.always_execute_both(action1=self._upload_engine.start_transfers,
                                        action2=self._download_engine.start_transfers)

    def stop_transfers(self) -> None:
        """
        Stops yellowdog object store client from transferring any new chunks for both upload and download. New transfers
        will be put on hold until :meth:`start` is used
        """
        ActionUtils.always_execute_both(action1=self._upload_engine.stop_transfers,
                                        action2=self._download_engine.stop_transfers)

    def abort_all_transfers(self) -> None:
        """
        Aborts all running transfers in object store client
        """
        ActionUtils.always_execute_both(
            self._upload_engine.abort_all_transfers,
            self._download_engine.abort_all_transfers
        )

    def clear_inactive_sessions(self) -> None:
        """
        Removes any inactive sessions from the list for both upload and download.
        """
        ActionUtils.always_execute_both(
            action1=self._upload_engine.clear_inactive_sessions,
            action2=self._download_engine.clear_inactive_sessions
        )

    def get_object_detail(self, namespace: str, name: str) -> ObjectDetail:
        """
        Returns details of stored file within the namespace in ``object store``

        :param namespace: file name of the file to query
        :param name: storage namespace within ``object store``
        :return: details about the remote file
        """
        return self._service_proxy.get_object_detail(namespace=namespace, object_name=name)

    def check_object_exists(self, namespace: str, name: str) -> bool:
        return self._service_proxy.check_object_exists(namespace=namespace, object_name=name)

    def get_namespaces(self) -> List[str]:
        """
        Returns a list of all namespaces in ``object store``

        :return: all namespaces
        """
        return self._service_proxy.get_namespaces()

    def get_namespace_object_paths(self, request: ObjectPathsRequest) -> List[ObjectPath]:
        """
        Returns a list of all stored objects within namespace in ``object store``

        :param request: the request
        :return: object paths within the namespace
        """
        return self._service_proxy.get_namespace_object_paths(request)

    def get_namespace_object_paths_slice(self, request: ObjectPathsSliceRequest) -> Slice[ObjectPath]:
        """
        Returns a slice of stored objects within namespace in ``object store``

        :param request: the request
        :return: object paths within the namespace
        """
        return self._service_proxy.get_namespace_object_paths_slice(request)

    def delete_objects(self, namespace: str, object_paths: Union[ObjectPath, List[ObjectPath]]) -> None:
        """
        Delete a collection of files within ``object store`` namespace

        :param namespace: namespace, holding a collection of objects
        :param object_paths: a collection of object names to delete
        """
        if isinstance(object_paths, ObjectPath):
            object_paths = [object_paths]

        self._service_proxy.delete_objects(namespace=namespace, object_paths=object_paths)

    def put_namespace_storage_configuration(self, namespace_storage_configuration: NamespaceStorageConfiguration) -> NamespaceStorageConfiguration:
        """
        Stores cloud provider storage configuration within ``YellowDog object store``

        :param namespace_storage_configuration: storage configuration for cloud provider
        :type namespace_storage_configuration: :class:`yellowdog_client.model.NamespaceStorageConfiguration`
        """
        return self._service_proxy.put_namespace_storage_configuration(namespace_storage_configuration)

    def delete_namespace_storage_configuration(self, namespace: str) -> None:
        """
        Removes all cloud provider storage configurations within namespace in ``YellowDog object store``

        :param namespace: namespace, holding storage configurations
        :type namespace: str
        """
        self._service_proxy.delete_namespace_storage_configuration(namespace=namespace)

    def get_namespace_storage_configurations(self) -> List[NamespaceStorageConfiguration]:
        """
        Returns all available storage configurations found within ``YellowDog object store``

        :return: cloud provider storage configurations
        :rtype: List[:class:`yellowdog_client.model.NamespaceStorageConfiguration`]
        """
        return self._service_proxy.get_namespace_storage_configurations()

    def _dispatch_error_notification(self, event_args: ClientErrorEventArgs) -> None:
        self._notification_dispatcher.dispatch(event_handler=self._on_error, event_args=event_args)

    @dispatch_async
    def _on_error(self, event_args: ClientErrorEventArgs) -> None:
        return self.emit(name=self.ON_ERROR, event_args=event_args)

    def _close(self, disposing: bool) -> None:
        if not self._disposed_value:
            if disposing:
                self.abort_all_transfers()
            self._disposed_value = True

    def close(self) -> None:
        """
        Aborts all transfers for upload and download. When executing :meth:`__exit__`, method :meth:`close` is invoked
        """
        self._close(disposing=True)
