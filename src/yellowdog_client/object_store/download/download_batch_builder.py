import fnmatch
from typing import Optional, List, Tuple

from yellowdog_client.model import ObjectPathsRequest
from yellowdog_client.model.exceptions import ErrorType
from yellowdog_client.model import FlattenPath
from yellowdog_client.object_store.abstracts import AbstractObjectStoreServiceProxy
from yellowdog_client.object_store.abstracts import AbstractSession
from yellowdog_client.object_store.abstracts import AbstractTransferBatch
from yellowdog_client.object_store.model import FileTransferException
from yellowdog_client.object_store.utils import FnmatchUtils
from .abstracts import AbstractDownloadBatchBuilder
from .abstracts import AbstractDownloadEngine
from .download_batch import DownloadBatch


class ObjectEntry(object):
    namespace: str = None
    object_name: str = None

    def __init__(self, namespace: str, object_name: str) -> None:
        self.namespace = namespace
        self.object_name = object_name

    def __eq__(self, other: 'ObjectEntry') -> bool:
        return self.namespace == other.namespace and self.object_name == other.object_name


class DownloadBatchBuilder(AbstractDownloadBatchBuilder):
    """
    Builder class for creating batch download from object store namespace

    .. versionadded:: 0.5.0

    .. seealso::

        Inherits from :class:`yellowdog_client.object_store.download.abstracts.AbstractDownloadBatchBuilder`
    """

    def __init__(self, download_engine: AbstractDownloadEngine, service_proxy: AbstractObjectStoreServiceProxy) -> None:
        self._download_engine: AbstractDownloadEngine = download_engine
        self._service_proxy: AbstractObjectStoreServiceProxy = service_proxy
        self._source_object_entries: List[ObjectEntry] = []
        self.set_flatten_file_name_mapper(value=None)

    def set_flatten_file_name_mapper(self, value: Optional[FlattenPath]) -> None:
        """
        Sets the method, which is used to rename files once they are downloaded in target directory

        :param value: enum value, indicating the method of path flattening
        :type value: Optional[:class:`yellowdog_client.model.FlattenPath`]
        """
        if value is None:
            self.flatten_file_name_mapper = None
        elif value == FlattenPath.FILE_NAME_ONLY:
            self.flatten_file_name_mapper = self._map_file_name_only
        elif value == FlattenPath.REPLACE_PATH_SEPERATOR:
            self.flatten_file_name_mapper = self._map_replace_path_separator
        else:
            raise ValueError("Unrecognised flatten path value: %s" % str(value))

    @staticmethod
    def _map_file_name_only(object_name: str) -> str:
        last_slash_index = object_name.rfind("/")
        return object_name[last_slash_index + 1:] if last_slash_index > -1 else object_name

    @staticmethod
    def _map_replace_path_separator(object_name: str) -> str:
        return object_name.replace("/", "_")

    def _create_download_session(self, object_entry: ObjectEntry, destination_file_names: List[str]) -> Tuple[
        AbstractSession, List[str]]:
        destination_file_name = object_entry.object_name

        # apply general file name mapper first
        if self.file_name_mapper is not None:
            destination_file_name = self.file_name_mapper(destination_file_name)

        # then apply flatten file name mapper
        if self.flatten_file_name_mapper is not None:
            destination_file_name = self.flatten_file_name_mapper(destination_file_name)

        if destination_file_name in destination_file_names:
            raise FileTransferException(
                ErrorType.InvalidRequestException,
                "Duplicated download file name would result in a conflict: %s" % destination_file_name
            )
        else:
            destination_file_names.append(destination_file_name)

        return self._download_engine.create_download_session(
            file_namespace=object_entry.namespace,
            file_name=object_entry.object_name,
            destination_folder_path=self.destination_folder,
            destination_file_name=destination_file_name,
            transfer_properties=self.transfer_properties
        ), destination_file_names

    def find_source_objects(self, namespace: str, object_name_pattern: str) -> None:
        """
        Iterates through all files found in remote namespace and its subdirectories. If files match the pattern, they
        are appended to list of files for download::

            builder.find_source_objects("MY_REMOTE_NAMESPACE", "*.txt")

        :param namespace: Object store namespace, containing required files
        :type namespace: str
        :param object_name_pattern: String, containing unix shell-style wildcards. See more at :mod:`fnmatch`
        :type object_name_pattern: str
        """
        if "\\" in object_name_pattern:
            raise ValueError("Only Unix style path separators ('/') should be used")

        if FnmatchUtils.uses_path_pattern(object_name_pattern):
            self._find_source_files_with_pattern(namespace, object_name_pattern)
        else:
            self._find_source_file(namespace, object_name_pattern)

    def _find_source_files_with_pattern(self, namespace: str, object_name_pattern: str) -> None:
        request = ObjectPathsRequest(
            namespace,
            prefix=FnmatchUtils.get_prefix_before_path_patterns(object_name_pattern),
            flat=True
        )

        object_paths = self._service_proxy.get_namespace_object_paths(request)
        for object_path in object_paths:
            object_name = object_path.name
            if fnmatch.fnmatch(object_name, object_name_pattern):
                self._source_object_entries.append(ObjectEntry(namespace=namespace, object_name=object_name))

    def _find_source_file(self, namespace: str, object_name: str) -> None:
        if self._service_proxy.check_object_exists(namespace, object_name):
            self._source_object_entries.append(ObjectEntry(namespace=namespace, object_name=object_name))

    def get_batch_if_objects_found(self) -> Optional[AbstractTransferBatch]:
        """
        Creates an download batch once download directory is set and download objects found using
        :meth:`find_source_objects`. Raises exception, if download directory is not set. Returns None, if no files are
        found for download

        :return: Download batch, containing all download sessions
        :rtype: Optional[:class:`yellowdog_client.object_store.download.DownloadBatch`]
        :raises: :class:`ValueError` if :attr:`destination_folder` is not set

        """
        if self.destination_folder is None:
            raise ValueError("Cannot build DownloadBatch without a destination_folder")

        if len(self._source_object_entries) == 0:
            return None

        download_sessions = []
        # noinspection PyBroadException
        try:
            destination_file_names = []
            for source_object_entry in self._source_object_entries:
                new_session, destination_file_names = self._create_download_session(
                    object_entry=source_object_entry,
                    destination_file_names=destination_file_names
                )
                download_sessions.append(new_session)
        except Exception:
            # abort any sessions that were created if an error has occurred
            [x.abort() for x in download_sessions]
            raise

        return DownloadBatch(sessions=download_sessions)
