from typing import List, Optional
import os
import fnmatch

from .upload_batch import UploadBatch
from .abstracts import AbstractUploadBatchBuilder
from .abstracts import AbstractUploadEngine
from yellowdog_client.model.exceptions import ErrorType
from yellowdog_client.object_store.abstracts import AbstractTransferBatch
from yellowdog_client.object_store.abstracts import AbstractSession
from yellowdog_client.object_store.model import FileTransferException


class UploadBatchBuilder(AbstractUploadBatchBuilder):
    """
    Builder class for creating batch upload for multiple files in directory

    .. versionadded:: 0.5.0

    .. seealso::

        Inherits from :class:`yellowdog_client.object_store.upload.abstracts.AbstractUploadBatchBuilder`
    """

    def __init__(self, upload_engine: AbstractUploadEngine) -> None:
        self._upload_engine: AbstractUploadEngine = upload_engine
        self._source_file_entries: List[FileEntry] = []

    def find_source_objects(self, source_directory_path: str, source_file_pattern: str) -> None:
        """
        Iterates through all files found in directory and its subdirectories. If files match the pattern, they are
        appended to list of files for upload::

            builder.find_source_objects("C:/my_files_for_upload", "*.txt")

        :param source_directory_path: Directory path to collect files for upload
        :type source_directory_path: str
        :param source_file_pattern: String, containing unix shell-style wildcards. See more at :mod:`fnmatch`
        :type source_file_pattern: str
        """
        for root, directories, file_names in os.walk(top=source_directory_path):
            relative_directory_path = os.path.relpath(root, source_directory_path)
            for file_name in file_names:
                file_path = os.path.join(root, file_name)
                if fnmatch.fnmatch(file_path, source_file_pattern):

                    source_file_path = file_path
                    if relative_directory_path == ".":
                        default_object_name = file_name
                    else:
                        default_object_name = os.path.join(relative_directory_path, file_name)
                    default_object_name = default_object_name.replace("\\", "/")
                    self._source_file_entries.append(
                        FileEntry(source_file_path=source_file_path, default_object_name=default_object_name)
                    )

    def _create_upload_session(self, file_entry: 'FileEntry', object_names: List[str]) -> AbstractSession:
        object_name = self.object_name_mapper(file_entry.default_object_name) \
            if self.object_name_mapper is not None \
            else file_entry.default_object_name

        if object_name in object_names:
            raise FileTransferException(
                error_type=ErrorType.FileTransferFailure,
                message="Duplicated upload object name would result in a conflict: %s" % object_name
            )

        object_names.append(object_name)

        if self.transfer_properties is not None:
            return self._upload_engine.create_upload_session(
                file_namespace=self.namespace,
                source_file_path=file_entry.source_file_path,
                destination_file_name=object_name,
                transfer_properties=self.transfer_properties
            )
        else:
            return self._upload_engine.create_upload_session(
                file_namespace=self.namespace,
                source_file_path=file_entry.source_file_path,
                destination_file_name=object_name
            )

    def get_batch_if_objects_found(self) -> Optional[AbstractTransferBatch]:
        """
        Creates an upload batch once namespace is set and upload objects found using :meth:`find_source_objects`.
        Raises exception, if namespace is not set. Returns None, if no files are found for upload

        :return: Upload batch, containing all upload sessions
        :rtype: Optional[:class:`yellowdog_client.object_store.upload.UploadBatch`]
        :raises: :class:`ValueError` if :attr:`namespace` is not set

        """

        if not self.namespace:
            raise ValueError("Cannot build UploadBatch without a namespace")

        if len(self._source_file_entries) == 0:
            return None

        upload_sessions = []
        # noinspection PyBroadException
        try:
            object_names = []
            for source_file_entry in self._source_file_entries:
                upload_sessions.append(
                    self._create_upload_session(
                        file_entry=source_file_entry, object_names=object_names
                    )
                )
        except Exception:
            [session.abort() for session in upload_sessions]
            raise

        return UploadBatch(sessions=upload_sessions)


class FileEntry(object):
    source_file_path: str = None
    default_object_name: str = None

    def __init__(self, source_file_path: str, default_object_name: str) -> None:
        self.source_file_path = source_file_path
        self.default_object_name = default_object_name

    def __eq__(self, other: 'FileEntry') -> bool:
        return self.source_file_path == other.source_file_path and self.default_object_name == other.default_object_name
