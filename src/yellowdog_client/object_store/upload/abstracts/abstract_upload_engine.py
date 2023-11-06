from typing import Optional

from yellowdog_client.object_store.abstracts import AbstractSession
from yellowdog_client.object_store.abstracts import AbstractTransferEngine
from yellowdog_client.object_store.model import TransferProperties

from .abstract_upload_batch_builder import AbstractUploadBatchBuilder


class AbstractUploadEngine(AbstractTransferEngine):
    def build_upload_batch(self) -> AbstractUploadBatchBuilder:
        raise NotImplementedError("Needs implementation")

    def create_upload_session(
            self,
            file_namespace: str,
            source_file_path: str,
            destination_file_name: str,
            transfer_properties: Optional[TransferProperties] = None
    ) -> AbstractSession:
        raise NotImplementedError("Needs implementation")
