from typing import Optional

from yellowdog_client.object_store.abstracts import AbstractTransferEngine
from yellowdog_client.object_store.abstracts import AbstractSession
from yellowdog_client.object_store.model import TransferProperties
from .abstract_download_batch_builder import AbstractDownloadBatchBuilder


class AbstractDownloadEngine(AbstractTransferEngine):
    def build_download_batch(self) -> AbstractDownloadBatchBuilder:
        raise NotImplementedError("Needs implementation")

    def create_download_session(
            self,
            file_namespace: str,
            file_name: str,
            destination_folder_path: str,
            destination_file_name: Optional[str] = None,
            transfer_properties: Optional[TransferProperties] = None
    ) -> AbstractSession:
        raise NotImplementedError("Needs implementation")
