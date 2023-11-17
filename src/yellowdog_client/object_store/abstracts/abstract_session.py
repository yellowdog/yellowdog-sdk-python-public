import os
from concurrent.futures import Future
from datetime import timedelta
from threading import Lock
from typing import Optional, Dict, List, Callable, Set, cast

import time
from cancel_token import CancellationToken
from pydispatch import Dispatcher

from yellowdog_client.common import CountdownEvent, Closeable
from yellowdog_client.model.exceptions import ErrorType
from yellowdog_client.object_store.model import FileTransferDirection
from yellowdog_client.object_store.model import FileTransferErrorEventArgs
from yellowdog_client.object_store.model import FileTransferEventArgs
from yellowdog_client.object_store.model import FileTransferException
from yellowdog_client.object_store.model import FileTransferProgressEventArgs
from yellowdog_client.object_store.model import FileTransferStatus
from yellowdog_client.object_store.model import TransferStatistics
from yellowdog_client.object_store.utils.hash_utils import HashUtils
from .abstract_chunk_transfer_task import AbstractChunkTransferTask
from .abstract_self_binding_status_predicate import SelfBindingStatusMatchPredicate
from .abstract_service_session_facade import AbstractServiceSessionFacade as SessionFacade


class AbstractSession(Closeable, Dispatcher, SelfBindingStatusMatchPredicate):
    """
    Base class for transfer session (upload and download). Inherits :class:`pydispatch.Dispatcher`

    Can be binded with callbacks on exceptions:

    :param event_args: session error arguments
    :type event_args: :class:`yellowdog_client.object_store.model.FileTransferErrorEventArgs`
    :callback: ``on_error``

        .. code-block:: python

            session.bind(on_error=lambda event_args: print(event_args.message))

    Can be binded with callbacks on status changes:

    :param event_args: session status change arguments
    :type event_args: :class:`yellowdog_client.object_store.model.FileTransferEventArgs`
    :callback: ``on_status_changed``

        .. code-block:: python

            session.bind(on_status_changed=lambda event_args: print(event_args.transfer_status))

    Can be binded with callbacks on session progress:

    :param event_args: session progress arguments
    :type event_args: :class:`yellowdog_client.object_store.model.FileTransferProgressEventArgs`
    :callback: ``on_progress``

        .. code-block:: python

            session.bind(on_progress=lambda event_args: print(event_args.transfer_status.transfer_percentage))

    .. versionadded:: 0.5.0
    """

    ON_ERROR = "on_error"
    ON_PROGRESS = "on_progress"
    ON_STATUS_CHANGED = "on_status_changed"
    _events_ = [ON_ERROR, ON_PROGRESS, ON_STATUS_CHANGED]
    _chunk_task_type: type = None
    _file_io: Optional[Closeable] = None

    file_path: str = None
    """
    File path of object being transferred
    
    :type: str
    """

    file_name: str = None
    """
    File name of object being transferred
    
    :type: str
    """

    file_size: int = None
    """
    File size in bytes of object being transferred
    
    :type: int
    """

    direction: FileTransferDirection = None
    """
    File transfer direction
    
    :type: :class:`yellowdog_client.object_store.model.FileTransferDirection`
    """

    def __init__(
            self,
            direction: FileTransferDirection,
            service_session_facade: SessionFacade,
            file_path: str,
            file_size: int,
            chunk_size: int,
            chunk_count: int,
            file_retry_count: int
    ) -> None:
        super(AbstractSession, self).__init__()
        self._service_session_facade: SessionFacade = service_session_facade
        self.file_path = file_path
        self.file_name = os.path.basename(self.file_path)
        self.file_size = file_size
        self.direction = direction
        self._chunk_size: int = chunk_size
        self._chunk_count: int = chunk_count
        self._last_chunk_size: int = self.calculate_last_chunk_size(
            chunk_size=chunk_size, chunk_count=chunk_count, file_size=file_size
        )
        self._file_retry_count: int = file_retry_count

        self._abort_token_source: CancellationToken = CancellationToken()
        self._abort_lock: Lock = Lock()
        self._file_io: Optional[Closeable] = None
        self._when_status_matches_lock: Lock = Lock()
        self._when_status_matches_predicates: Dict[Future, Callable[[FileTransferStatus], bool]] = {}
        self._chunk_hashes: Dict[int, str] = {}
        self._bytes_transferred_lock: Lock = Lock()
        self._bytes_transferred: int = 0
        self._session_start: Optional[float] = None
        self._session_stop: Optional[float] = None
        self._status: FileTransferStatus = FileTransferStatus.Ready
        # To detect redundant calls
        self._disposed_value: bool = False

    @property
    def elapsed(self) -> timedelta:
        """
        :return: Time duration, since the session was started
        :rtype: :class:`datetime.timedelta`
        """
        if not self._session_start and not self._session_stop:
            return timedelta()
        elif self._session_start and not self._session_stop:
            sec_diff = time.time() - self._session_start
            return timedelta(seconds=sec_diff)
        elif self._session_start and self._session_stop:
            sec_diff = self._session_stop - self._session_start
            return timedelta(seconds=sec_diff)
        else:
            return timedelta()

    @property
    def bytes_transferred(self) -> int:
        """
        :return: A number of bytes transferred during the session
        :rtype: int
        """
        with self._bytes_transferred_lock:
            return self._bytes_transferred

    @bytes_transferred.setter
    def bytes_transferred(self, value: int) -> None:
        with self._bytes_transferred_lock:
            self._bytes_transferred = value

    @property
    def status(self) -> FileTransferStatus:
        """
        :return: Latest status of transfer session
        :rtype: :class:`yellowdog_client.object_store.model.FileTransferStatus`
        """
        return self._status

    @status.setter
    def status(self, value: FileTransferStatus) -> None:
        if self._status is not None:
            self._status = value
            self._notify_on_status_changed(status=self._status)

    def _release_file(self):
        if self._file_io is not None:
            self._file_io.close()
            self._file_io = None

    def _build_chunk_task(self, chunk_number: int, chunk_size: int,
                          transfer_countdown: CountdownEvent) -> AbstractChunkTransferTask:
        task = self._chunk_task_type()
        task.session_id = self._service_session_facade.session_id
        task.chunk_number = chunk_number
        task.chunk_size = chunk_size
        task.abort_token = self._abort_token_source
        task.abort_lock = self._abort_lock
        task.transfer_countdown = transfer_countdown
        task.notify_chunk_transferred = lambda chunk_hash: self._on_chunk_transferred(
            chunk_number=chunk_number, chunk_size=chunk_size, chunk_hash=chunk_hash
        )
        task.notify_exception = self._notify_on_chunk_error

        self._on_build_chunk_transfer_task(task=task)

        return task

    def _reset_bytes_transferred(self, transferred_chunks: List[int]) -> None:
        if len(transferred_chunks) > 0:
            if self._chunk_count in transferred_chunks:
                self.bytes_transferred = ((len(transferred_chunks) - 1) * self._chunk_size) + self._last_chunk_size
            else:
                self.bytes_transferred = len(transferred_chunks) * self._chunk_size
        else:
            self._bytes_transferred = 0

    def _transfer_chunks(self, chunk_numbers: List[int], abort_token: CancellationToken,
                         enqueue_chunk_task_method: Callable[[AbstractChunkTransferTask], None]) -> List[int]:

        chunk_count = len(chunk_numbers)

        if chunk_count > 0:
            # init the countdown event to the number of chunks still to transfer
            chunk_countdown = CountdownEvent(count=len(chunk_numbers))

            # enqueue the tasks to transfer the chunks, they will then be handled asynchronously by the transfer engine
            for chunk_number in chunk_numbers:
                chunk_size = self._chunk_size if chunk_number < self._chunk_count else self._last_chunk_size
                enqueue_chunk_task_method(
                    self._build_chunk_task(
                        chunk_number=chunk_number,
                        chunk_size=chunk_size,
                        transfer_countdown=chunk_countdown
                    )
                )

            # now this thread waits on the countdown event for the transfer engine to have attempted all chunk transfers
            try:
                chunk_countdown.wait(cancellation_token=abort_token)
            except Exception as ex:
                print("Chunk transfer failed. %s" % str(ex))

        # now this thread waits on the countdown event for the transfer engine to have attempted all chunk transfers
        try:
            if abort_token.cancelled:
                return chunk_numbers

            transferred_chunks_from_facade = self._service_session_facade.server_chunks_transferred
            transferred_chunks_hash_keys = self._chunk_hashes.keys()
            transferred_chunks = [x for x in transferred_chunks_hash_keys if x in transferred_chunks_from_facade]

            chunk_numbers = [x for x in chunk_numbers if x not in transferred_chunks]
            if len(chunk_numbers) > 0:
                self._reset_bytes_transferred(transferred_chunks=transferred_chunks)
        except Exception as ex:
            print("Chunk transfer failed. %s" % str(ex))
        return chunk_numbers

    def transfer_chunks_with_retries(self,
                                     enqueue_chunk_task_method: Callable[[AbstractChunkTransferTask], None]) -> None:
        try:
            abort_token = self._abort_token_source
            chunk_numbers = [x for x in range(1, self._chunk_count + 1)]

            chunk_numbers = self._transfer_chunks(
                chunk_numbers=chunk_numbers,
                abort_token=abort_token,
                enqueue_chunk_task_method=enqueue_chunk_task_method
            )

            retry = 0
            while len(chunk_numbers) > 0 and retry < self._file_retry_count and not abort_token.cancelled:
                retry += 1
                self._notify_on_error(
                    error_type=ErrorType.ChunkTransferException,
                    message="%s chunks failed to transfer. Retry %s out of %s" % (
                        str(len(chunk_numbers)), str(retry), str(self._file_retry_count)
                    )
                )
                chunk_numbers = self._transfer_chunks(
                    chunk_numbers=chunk_numbers,
                    abort_token=abort_token,
                    enqueue_chunk_task_method=enqueue_chunk_task_method
                )

            if abort_token.cancelled:
                return

            if len(chunk_numbers) == 0:
                if len(self._chunk_hashes) == self._chunk_count:
                    try:
                        self._complete()
                    except Exception as ex_any:
                        self._notify_on_exception(exception=ex_any)
                        self._fail()
                else:
                    self._notify_on_error(
                        error_type=ErrorType.FileTransferFailure,
                        message="File transfer aborted due to internal chunk hash count mismatch"
                    )
                    self._fail()
            else:
                self._notify_on_error(
                    error_type=ErrorType.FileTransferFailure,
                    message="File transfer aborted as %s chunks failed to transfer after %s retries" %
                            (str(len(chunk_numbers)), self._file_retry_count)
                )
                self._fail()
        except Exception as ex:
            self._notify_on_exception(exception=ex)
            self._fail()

    def _notify_on_chunk_error(self, exception: Exception) -> None:
        self._notify_on_exception(exception=exception)

        # noinspection PyUnresolvedReferences
        if type(exception) == FileTransferException and exception.error_type.is_fatal_session_error():
            self._abort_transfer(final_status=FileTransferStatus.Failed, abort_server=False)

    def _notify_on_exception(self, exception: Exception) -> None:
        if type(exception) == FileTransferException:
            exception = cast(FileTransferException, exception)
            self._notify_on_error(
                error_type=exception.error_type,
                message=exception.message,
                detail=exception.detail
            )
        else:
            self._notify_on_error(
                error_type=ErrorType.Unknown,
                message=str(exception)
            )

    def _notify_on_error(self, error_type: ErrorType, message: str, detail: Optional[Set[str]] = None) -> None:
        if not detail:
            detail = set()

        event_args = FileTransferErrorEventArgs(
            full_path=self.file_path,
            file_name=self.file_name,
            transfer_status=self._status,
            error_type=error_type,
            message=message,
            detail=detail
        )

        self._service_session_facade.dispatch_notification(event_handler=self._on_error, event_args=event_args)

    def _on_error(self, event_args: FileTransferErrorEventArgs) -> None:
        return self.emit(name=self.ON_ERROR, event_args=event_args)

    def _notify_on_progress(self, bytes_transferred: int) -> None:
        self._bytes_transferred += bytes_transferred

        event_args = FileTransferProgressEventArgs(
            full_path=self.file_path,
            file_name=self.file_name,
            transfer_status=self.status,
            bytes_transferred=self.bytes_transferred,
            total_file_bytes=self.file_size,
            elapsed_time_delta=self.elapsed
        )

        self._service_session_facade.dispatch_notification(event_handler=self._on_progress, event_args=event_args)

    def _on_progress(self, event_args: FileTransferProgressEventArgs) -> None:
        return self.emit(name=self.ON_PROGRESS, event_args=event_args)

    def _notify_on_status_changed(self, status: FileTransferStatus) -> None:
        event_args = FileTransferEventArgs(
            full_path=self.file_path,
            file_name=self.file_name,
            transfer_status=status
        )

        self._service_session_facade.dispatch_notification(event_handler=self._on_status_changed, event_args=event_args)

    def _on_status_changed(self, event_args: FileTransferEventArgs) -> None:
        return self.emit(name=self.ON_STATUS_CHANGED, event_args=event_args)

    def _fail(self) -> None:
        try:
            self._release_file()
            self.status = FileTransferStatus.Failed
            self._service_session_facade.abort()
        except Exception as ex_any:
            self._notify_on_exception(exception=ex_any)

    def _on_chunk_transferred(self, chunk_number: int, chunk_size: int, chunk_hash: str) -> None:
        self._notify_on_progress(bytes_transferred=chunk_size)
        self._chunk_hashes[chunk_number] = chunk_hash

    def _on_build_chunk_transfer_task(self, task: AbstractChunkTransferTask) -> None:
        raise NotImplementedError("_on_build_chunk_transfer_task Needs implementation by subclass")

    def _calculate_chunk_offset(self, chunk_number: int) -> int:
        return self.calculate_chunk_offset(chunk_number=chunk_number, chunk_size=self._chunk_size)

    def _start_transfer_session(self, file_io: Closeable,
                                enqueue_chunk_task_method: Callable[[AbstractChunkTransferTask], None]) -> None:
        self._file_io = file_io
        self._session_end = None
        self._session_start = time.time()
        self._service_session_facade.create_thread(
            target=lambda: self.transfer_chunks_with_retries(enqueue_chunk_task_method=enqueue_chunk_task_method)
        ).start()
        if self.direction == FileTransferDirection.Download:
            self.status = FileTransferStatus.Downloading
        elif self.direction == FileTransferDirection.Upload:
            self.status = FileTransferStatus.Uploading

    def _start_transfer(self) -> None:
        raise NotImplementedError("_start_transfer Needs implementation by subclass")

    def start(self) -> None:
        """
        Starts transfer session, allowing transfer engine to proceed with chunk upload or download
        """
        if self.status != FileTransferStatus.Ready:
            return

        try:
            self._start_transfer()
        except Exception as ex:
            self._notify_on_exception(exception=ex)

    def _complete(self) -> None:
        self._release_file()
        self.status = FileTransferStatus.Validating
        chunk_hashes_keys = [x for x in self._chunk_hashes]
        sorted_chunk_hashes_keys = sorted(chunk_hashes_keys)
        sorted_chunk_hashes = [self._chunk_hashes[x] for x in sorted_chunk_hashes_keys]
        summary_hash = HashUtils.calculate_md5_summary_in_base_64_url(hashes_as_base_64=sorted_chunk_hashes)
        self._service_session_facade.complete(summary_hash=summary_hash)
        self._session_end = time.time()
        self._on_complete()
        self.status = FileTransferStatus.Completed

    def _on_complete(self) -> None:
        pass  # Can be overwritten by Subclass

    def _abort_transfer(self, final_status: FileTransferStatus, abort_server: bool) -> None:
        self._abort_token_source.cancel()

        with self._abort_lock:
            try:
                self._release_file()
                if abort_server:
                    self._service_session_facade.abort()
                self._session_end = time.time()
                self._on_abort()
                new_status = final_status
            except Exception as ex_any:
                self._notify_on_exception(exception=ex_any)
                new_status = FileTransferStatus.Failed

        self.status = new_status

    def when_status_matches(self, status_predicate: Callable[[FileTransferStatus], bool]) -> Future:
        """
        Assigns a session status predicate, which, when evaluates to True, sets a value for
        :class:`concurrent.futures.Future`::

            from concurrent import futures
            from yellowdog_client.object_store.model import FileTransferStatus

            future = session.when_status_matches(lambda status: status == FileTransferStatus.Completed)
            futures.wait(fs=(future,))  # Wait for session status to match Completed

        :param status_predicate: file transfer status predicate to wait for
        :type status_predicate: Callable[[:class:`yellowdog_client.object_store.model.FileTransferStatus`], bool]
        :return: a future to wait for session status to match a predicate
        :rtype: :class:`concurrent.futures.Future`
        """
        future = Future()
        future.set_running_or_notify_cancel()
        if status_predicate(self.status):
            future.set_result(result=self)
        else:
            # For some reason cannot assign lambda callback - weak reference list loses my binded callback. The only way
            # so far to fix this is by adding a method, which accepts no other arguments. Tried creating a class with
            # members - this does not work either
            with self._when_status_matches_lock:
                self._add_when_status_matches_future(future=future, predicate=status_predicate)

            self.bind(on_status_changed=self._when_status_matches_callback)
        return future

    def _when_status_matches_callback(self, event_args: FileTransferEventArgs) -> None:
        with self._when_status_matches_lock:
            futures_and_predicates_dict = self._get_when_status_matches_futures()
            for future in futures_and_predicates_dict:
                predicate = futures_and_predicates_dict[future]
                if not future.done() and predicate(event_args.transfer_status):
                    future.set_result(result=self)
                    self._remove_when_status_matches_future(future=future)

    def get_statistics(self) -> TransferStatistics:
        """
        Calculates transfer statistics for transfer session

        :return: Calculated statistics of file upload or download
        :rtype: :class:`yellowdog_client.object_store.model.TransferStatistics`
        """
        return TransferStatistics(
            bytes_transferred=self.bytes_transferred, total_bytes=self.file_size,
            elapsed_millis=self.elapsed.microseconds / 1000
        )

    def abort(self) -> None:
        """
        Aborts any ongoing chunk transfers and prevents from continuing with new chunk transfers
        """
        self._abort_transfer(final_status=FileTransferStatus.Aborted, abort_server=True)

    def _on_abort(self) -> None:
        # Needs implementation by Subclass
        pass

    def _close(self, disposing: bool) -> None:
        if not self._disposed_value:
            if disposing:
                self._release_file()
            self._disposed_value = True

    def close(self) -> None:
        """
        Closes the session and releases any resources related to file transfer
        """
        self._close(disposing=True)

    @staticmethod
    def calculate_last_chunk_size(chunk_size: int, chunk_count: int, file_size: int) -> int:
        return file_size - (chunk_size * (chunk_count - 1))

    @staticmethod
    def calculate_chunk_offset(chunk_number, chunk_size):
        return (chunk_number - 1) * chunk_size
