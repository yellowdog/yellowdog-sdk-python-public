from typing import List, Tuple, Optional
from urllib.parse import quote

from pydispatch import Dispatcher

from yellowdog_client.common.json import Json
from yellowdog_client.model import ObjectPath, Slice, ObjectPathsSliceRequest, ObjectPathsRequest, SliceReference
from yellowdog_client.common import Proxy
from yellowdog_client.common.decorators.dispatcher import dispatch_async
from yellowdog_client.model import ObjectDetail
from yellowdog_client.model import ObjectDownloadRequest
from yellowdog_client.model import ObjectDownloadResponse
from yellowdog_client.model import ObjectUploadRequest
from yellowdog_client.model import TransferStatusResponse
from yellowdog_client.model import NamespaceStorageConfiguration
from yellowdog_client.object_store.model import ClientErrorEventArgs
from .abstracts import AbstractObjectStoreServiceProxy


class ObjectStoreServiceProxy(AbstractObjectStoreServiceProxy, Dispatcher):
    ON_ERROR = "on_error"
    _events_ = [ON_ERROR]

    def __init__(
            self,
            proxy: Proxy,
            request_timeout_ms: int = 10 * 1000,
            request_upload_chunk_timeout_ms: int = 20 * 60 * 1000,
            request_download_chunk_timeout_ms: int = 20 * 60 * 1000
    ) -> None:
        super(ObjectStoreServiceProxy, self).__init__(None, None)
        self._request_timeout_ms: int = request_timeout_ms
        self._request_upload_chunk_timeout_ms: int = request_upload_chunk_timeout_ms
        self._request_download_chunk_timeout_ms: int = request_download_chunk_timeout_ms
        self._proxy: Proxy = proxy.append_base_url("/objectstore/")

    def start_upload_session(self, namespace: str, object_upload_request: ObjectUploadRequest) -> str:
        json = Json.dump(object_upload_request)
        return self._proxy.raw_execute('POST', "objects/%s/startUpload" % namespace, json).text

    def start_download_session(self, namespace: str,
                               object_download_request: ObjectDownloadRequest) -> ObjectDownloadResponse:
        return self._proxy.post(ObjectDownloadResponse, object_download_request, "objects/%s/startDownload" % namespace)

    def abort_transfer(self, session_id: str) -> None:
        self._proxy.delete("transfers/%s/abort" % session_id)

    def complete_transfer(self, session_id: str, summary_hash: str) -> None:
        self._proxy.post(url="transfers/%s/complete" % session_id, params={'summaryHash': summary_hash})

    def get_transfer_status(self, session_id: str) -> TransferStatusResponse:
        return self._proxy.get(TransferStatusResponse, "transfers/%s" % session_id)

    def get_object_detail(self, namespace: str, object_name: str) -> ObjectDetail:
        return self._proxy.get(ObjectDetail, "objects/%s/object" % namespace, params={'name': object_name})

    def check_object_exists(self, namespace: str, object_name: str) -> bool:
        return self._proxy.get(bool, "objects/%s/object/exists" % namespace, params={'name': object_name})

    def get_namespaces(self) -> List[str]:
        return self._proxy.get(List[str], "objects")

    def get_namespace_object_paths(self, request: ObjectPathsRequest) -> List[ObjectPath]:
        object_paths_slice = self.get_namespace_object_paths_slice(self._sliced(request, SliceReference()))
        object_paths = object_paths_slice.items

        while object_paths_slice.nextSliceId is not None:
            object_paths_slice = self.get_namespace_object_paths_slice(
                self._sliced(request, SliceReference(object_paths_slice.nextSliceId)))
            object_paths += object_paths_slice.items

        return object_paths

    @staticmethod
    def _sliced(request: ObjectPathsRequest, slice_reference: SliceReference):
        return ObjectPathsSliceRequest(request.namespace, request.flat, request.prefix, slice_reference)

    def get_namespace_object_paths_slice(self, request: ObjectPathsSliceRequest) -> Slice[ObjectPath]:
        params = {'size': request.sliceReference.size}

        if request.sliceReference.sliceId:
            params['sliceId'] = request.sliceReference.sliceId

        if request.prefix:
            params['prefix'] = request.prefix

        if request.flat:
            params['flat'] = True

        return self._proxy.get(Slice[ObjectPath], "objects/%s" % request.namespace, params)

    def delete_objects(self, namespace: str, object_paths: List[ObjectPath]) -> None:
        self._proxy.put(data=object_paths, url="objects/%s/delete" % namespace)

    def put_namespace_storage_configuration(
            self,
            conf: NamespaceStorageConfiguration
    ) -> NamespaceStorageConfiguration:
        return self._proxy.put(NamespaceStorageConfiguration, conf, "configurations")

    def delete_namespace_storage_configuration(self, namespace: str) -> None:
        self._proxy.delete("configurations/%s" % namespace)

    def get_namespace_storage_configurations(self) -> List[NamespaceStorageConfiguration]:
        return self._proxy.get(List[NamespaceStorageConfiguration], "configurations")

    def upload_chunk(self, session_id: str, chunk_number: str, chunk_data: str, chunk_hash: str) -> None:
        encoded_session_id = quote(session_id)
        self._proxy.execute_with_timeout(
            "PUT",
            self._request_upload_chunk_timeout_ms,
            "transfers/%s/chunks/%s" % (encoded_session_id, chunk_number),
            chunk_data,
            {
                'content-type': 'application/octet-stream',
                'content-length': str(len(chunk_data)),
                'content-md5': chunk_hash
            }
        )

    def download_chunk(self, session_id: str, chunk_number: int, chunk_size: int, chunk_hash: str) -> Tuple[
        bytes, Optional[str]]:
        encoded_session_id = quote(session_id)
        response = self._proxy.execute_with_timeout(
            "GET",
            self._request_download_chunk_timeout_ms,
            "transfers/%s/chunks/%s" % (encoded_session_id, chunk_number)
        )
        response_chunk_hash = response.headers.get("Content-MD5")
        return response.content, response_chunk_hash

    @dispatch_async
    def _on_error(self, event_args: ClientErrorEventArgs) -> None:
        return self.emit(name=self.ON_ERROR, event_args=event_args)
