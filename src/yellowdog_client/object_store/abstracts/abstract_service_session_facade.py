from typing import Callable, List

from .abstract_object_store_service_proxy import AbstractObjectStoreServiceProxy
from .abstract_chunk_transfer_task import AbstractChunkTransferTask
from .abstract_notification_dispatcher import AbstractNotificationDispatcher
from yellowdog_client.object_store.utils import BackgroundThreadFactory
from yellowdog_client.object_store.utils import BackgroundThread
from yellowdog_client.object_store.model import FileTransferEventArgs


class AbstractServiceSessionFacade(object):
    session_id: str = None
    object_store_service_proxy: AbstractObjectStoreServiceProxy = None
    thread_factory: BackgroundThreadFactory = None
    notification_dispatcher: AbstractNotificationDispatcher = None

    def enqueue_chunk_upload(self, chunk_upload_task: AbstractChunkTransferTask) -> None:
        raise NotImplementedError("enqueue_chunk_upload Needs implementation")

    def enqueue_chunk_download(self, chunk_download_task: AbstractChunkTransferTask) -> None:
        raise NotImplementedError("enqueue_chunk_download Needs implementation")

    def abort(self) -> None:
        raise NotImplementedError("abort Needs implementation")

    def complete(self, summary_hash: str) -> None:
        raise NotImplementedError("complete Needs implementation")

    @property
    def server_chunks_transferred(self) -> List[int]:
        raise NotImplementedError("server_chunks_transferred Needs implementation")

    def create_thread(self, target: Callable) -> BackgroundThread:
        raise NotImplementedError("create_thread Needs implementation")

    def dispatch_notification(self, event_handler: Callable, event_args: FileTransferEventArgs) -> None:
        raise NotImplementedError("dispatch_notification Needs implementation")
