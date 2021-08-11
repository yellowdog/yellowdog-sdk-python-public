from typing import List, Set, Tuple, Optional

# noinspection PyPackageRequirements
from pydispatch import Dispatcher

from yellowdog_client.model import ObjectPath, ObjectPathsSliceRequest, ObjectPathsRequest
from yellowdog_client.common.decorators import dispatch_async
from yellowdog_client.model.exceptions import ErrorType
from yellowdog_client.model import ObjectDetail
from yellowdog_client.model import ObjectDownloadRequest
from yellowdog_client.model import ObjectDownloadResponse
from yellowdog_client.model import ObjectUploadRequest
from yellowdog_client.model import TransferStatusResponse
from yellowdog_client.model import NamespaceStorageConfiguration


class AbstractObjectStoreServiceProxy(Dispatcher):
    ON_ERROR = "on_error"
    _events_ = (ON_ERROR,)

    def start_upload_session(self, namespace, object_upload_request):
        # type: (str, ObjectUploadRequest) -> str
        raise NotImplementedError("start_upload_session Needs implementation")

    def start_download_session(self, namespace, object_download_request):
        # type: (str, ObjectDownloadRequest) -> ObjectDownloadResponse
        raise NotImplementedError("start_download_session Needs implementation")

    def abort_transfer(self, session_id):
        # type: (str) -> None
        raise NotImplementedError("abort_transfer Needs implementation")

    def complete_transfer(self, session_id, summary_hash):
        # type: (str, str) -> None
        raise NotImplementedError("complete_transfer Needs implementation")

    def get_transfer_status(self, session_id):
        # type: (str) -> TransferStatusResponse
        raise NotImplementedError("get_transfer_status Needs implementation")

    def get_object_detail(self, namespace, object_name):
        # type: (str, str) -> ObjectDetail
        raise NotImplementedError("get_object_detail Needs implementation")

    def get_namespace_object_paths(self, request):
        # type: (ObjectPathsRequest) -> List[ObjectPath]
        raise NotImplementedError("get_namespace_object_paths Needs implementation")

    def get_namespace_object_paths_slice(self, request):
        # type: (ObjectPathsSliceRequest) -> List[ObjectPath]
        raise NotImplementedError("get_namespace_object_paths Needs implementation")

    def delete_objects(self, namespace, object_paths):
        # type: (str, List[ObjectPath]) -> None
        raise NotImplementedError("delete_objects Needs implementation")

    def upload_chunk(self, session_id, chunk_number, chunk_data, chunk_hash):
        # type: (str, int, str, str) -> None
        raise NotImplementedError("upload_chunk Needs implementation")

    def download_chunk(self, session_id, chunk_number, chunk_size, chunk_hash):
        # type: (str, int, int, str) -> Tuple[bytes, Optional[str]]
        raise NotImplementedError("download_chunk Needs implementation")

    def put_namespace_storage_configuration(self, namespace_storage_configuration):
        # type: (NamespaceStorageConfiguration) -> None
        raise NotImplementedError("put_namespace_storage_configuration Needs implementation")

    def delete_namespace_storage_configuration(self, namespace):
        # type: (str) -> None
        raise NotImplementedError("delete_namespace_storage_configuration Needs implementation")

    def get_namespace_storage_configurations(self):
        # type: () -> List[NamespaceStorageConfiguration]
        raise NotImplementedError("get_namespace_storage_configurations Needs implementation")

    @dispatch_async
    def _on_error(self, error_type, message, detail):
        # type: (ErrorType, str, Set[str]) -> None
        self.emit(name=self.ON_ERROR, error_type=error_type, message=message, detail=detail)
