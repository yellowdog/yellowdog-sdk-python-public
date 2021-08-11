from typing import List, Callable

from .utils import BackgroundThread
from .abstracts import AbstractServiceSessionFacade
from .abstracts import AbstractChunkUploadTask
from .abstracts import AbstractChunkDownloadTask
from .abstracts import AbstractTransferEngine
from .model import FileTransferEventArgs


class ServiceSessionFacade(AbstractServiceSessionFacade):
    upload_engine = None            # type: AbstractTransferEngine
    download_engine = None          # type: AbstractTransferEngine

    def enqueue_chunk_upload(self, chunk_upload_task):
        # type: (AbstractChunkUploadTask) -> None
        self.upload_engine.enqueue_chunk_transfer_task(chunk_task=chunk_upload_task)

    def enqueue_chunk_download(self, chunk_download_task):
        # type: (AbstractChunkDownloadTask) -> None
        self.download_engine.enqueue_chunk_transfer_task(chunk_task=chunk_download_task)

    def abort(self):
        # type: () -> None
        self.object_store_service_proxy.abort_transfer(session_id=self.session_id)

    def complete(self, summary_hash):
        # type: (str) -> None
        self.object_store_service_proxy.complete_transfer(session_id=self.session_id, summary_hash=summary_hash)

    @property
    def server_chunks_transferred(self):
        # type: () -> List[int]
        return self.object_store_service_proxy.get_transfer_status(session_id=self.session_id).chunksReceived

    def create_thread(self, target):
        # type: (Callable) -> BackgroundThread
        return self.thread_factory.new_thread(target=target)

    def dispatch_notification(self, event_handler, event_args):
        # type: (Callable, FileTransferEventArgs) -> None
        self.notification_dispatcher.dispatch(event_handler=event_handler, event_args=event_args)
