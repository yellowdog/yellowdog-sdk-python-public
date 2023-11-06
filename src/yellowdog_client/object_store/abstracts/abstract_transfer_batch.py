from typing import List, Callable, Dict
from threading import Lock
from concurrent.futures import Future

from pydispatch import Dispatcher

from .abstract_self_binding_status_predicate import SelfBindingStatusMatchPredicate
from yellowdog_client.object_store.model import FileTransferDirection
from yellowdog_client.object_store.model import FileTransferStatus
from yellowdog_client.object_store.model import TransferStatistics
from yellowdog_client.object_store.model import FileTransferEventArgs
from yellowdog_client.object_store.model import FileTransferProgressEventArgs
from yellowdog_client.object_store.model import FileTransferErrorEventArgs
from yellowdog_client.object_store.model import BatchTransferEventArgs
from .abstract_session import AbstractSession


class AbstractTransferBatch(Dispatcher, SelfBindingStatusMatchPredicate):
    """
    Base class for transfer batch (a collection of multiple uploads or downloads).
    Inherits :class:`pydispatch.Dispatcher`

    Can be binded with callbacks on status changes:

    :param event_args: transfer batch status change arguments
    :type event_args: :class:`yellowdog_client.object_store.model.BatchTransferEventArgs`
    :callback: ``on_status_changed``

        .. code-block:: python

            batch.bind(on_status_changed=lambda event_args: print(event_args.transfer_status))

    .. versionadded:: 0.5.0
    """
    ON_STATUS_CHANGED = "on_status_changed"
    _events_ = [ON_STATUS_CHANGED]
    direction: FileTransferDirection = None
    """
    Batch transfer direction
    
    :type: :class:`yellowdog_client.object_store.model.FileTransferDirection`
    """

    status: FileTransferStatus = None
    """
    Status of batch transfer
    
    :rtype: :class:`yellowdog_client.object_store.model.FileTransferStatus`
    """

    def __init__(self, transfer_direction: FileTransferDirection, sessions: List[AbstractSession]) -> None:
        super(AbstractTransferBatch, self).__init__()
        self.direction = transfer_direction
        self._transfer_sessions: List[AbstractSession] = sessions
        self.status = FileTransferStatus.Ready
        self._when_status_matches_lock: Lock = Lock()
        self._when_status_matches_predicates: Dict[Future, Callable[[FileTransferStatus], bool]] = {}

        self.add_session_status_listener(listener=self._notify_session_status)

    def _set_status(self, status: FileTransferStatus) -> None:
        if self.status != status:
            self.status = status
            self._on_status_changed(event_args=BatchTransferEventArgs(status=self.status))

    def _on_status_changed(self, event_args: BatchTransferEventArgs) -> None:
        self.emit(self.ON_STATUS_CHANGED, event_args=event_args)

    def _notify_session_status(self, event_args: FileTransferEventArgs) -> None:
        session_status = event_args.transfer_status
        if session_status in (FileTransferStatus.Uploading, FileTransferStatus.Downloading):
            if self.status == FileTransferStatus.Ready:
                self._set_status(status=session_status)
        elif session_status in (FileTransferStatus.Completed,):
            if all([x.status == FileTransferStatus.Completed for x in self._transfer_sessions]):
                self._set_status(status=FileTransferStatus.Completed)
        elif session_status in (FileTransferStatus.Failed,):
            if self.status.is_active():
                self._set_status(FileTransferStatus.Failed)
                self.abort()
        elif session_status in (FileTransferStatus.Aborted,) and self.status.is_active():
            self._set_status(status=FileTransferStatus.Aborted)
            self.abort()

    def start(self) -> None:
        """
        Starts batch transfer for uploads or downloads
        """
        # noinspection PyBroadException
        try:
            [session.start() for session in self._transfer_sessions]
        except Exception:
            self.abort()
            raise Exception("Unable to start all transfer sessions in batch")

    def abort(self) -> None:
        """
        Aborts all transfer sessions, stopping any further chunk uploads or downloads
        """
        # noinspection PyBroadException
        try:
            [session.abort() for session in self._transfer_sessions]
        except Exception:
            raise Exception("Unable to abort all transfer sessions in batch")

    def get_transfer_sessions(self) -> List[AbstractSession]:
        """
        :return: A collection of all transfer sessions within the batch
        :rtype: List[:class:`yellowdog_client.object_store.abstracts.AbstractSession`]
        """
        return [x for x in self._transfer_sessions]

    def add_session_status_listener(self, listener: Callable[[FileTransferEventArgs], None]) -> None:
        """
        Binds event callback to all sessions within batch for status changes

        :param listener: callback, which executes when any of session status changes
        :type listener: Callable[[:class:`yellowdog_client.object_store.model.FileTransferEventArgs`], None]

        .. code-block:: python

            batch.add_session_status_listener(lambda event_args: print(event_args.transfer_status))
        """
        [session.bind(on_status_changed=listener) for session in self._transfer_sessions]

    def add_session_progress_listener(self, listener: Callable[[FileTransferProgressEventArgs], None]) -> None:
        """
        Binds event callback to all sessions within batch for progress changes

        :param listener: callback, which executes when any of session progress changes
        :type listener: Callable[[:class:`yellowdog_client.object_store.model.FileTransferProgressEventArgs`], None]

        .. code-block:: python

            batch.add_session_progress_listener(lambda event_args: print(event_args.transfer_status.transfer_percentage))
        """
        [session.bind(on_progress=listener) for session in self._transfer_sessions]

    def add_session_error_listener(self, listener: Callable[[FileTransferErrorEventArgs], None]) -> None:
        """
        Binds event callback to all sessions within batch for errors

        :param listener: callback, which executes when any of session encounter error
        :type listener: Callable[[:class:`yellowdog_client.object_store.model.FileTransferErrorEventArgs`], None]

        .. code-block:: python

            batch.add_session_error_listener(lambda event_args: print(event_args.message))
        """
        [session.bind(on_error=listener) for session in self._transfer_sessions]

    def when_status_matches(self, status_predicate: Callable[[FileTransferStatus], bool]) -> Future:
        """
        Assigns a transfer batch status predicate, which, when evaluates to True, sets a value for
        :class:`concurrent.futures.Future`::

            from concurrent import futures
            from yellowdog_client.object_store.model import FileTransferStatus

            future = batch.when_status_matches(lambda status: status == FileTransferStatus.Completed)
            futures.wait(fs=(future,))  # Wait for batch status to match Completed

        :param status_predicate: file transfer status predicate to wait for
        :type status_predicate: Callable[[:class:`yellowdog_client.object_store.model.FileTransferStatus`], bool]
        :return: a future to wait for batch status to match a predicate
        :rtype: :class:`concurrent.futures.Future`
        """
        future = Future()
        future.set_running_or_notify_cancel()
        if status_predicate(self.status):
            future.set_result(result=self)
        else:
            with self._when_status_matches_lock:
                self._add_when_status_matches_future(future=future, predicate=status_predicate)

            self.bind(on_status_changed=self._when_status_matches_callback)
        return future

    def _when_status_matches_callback(self, event_args: BatchTransferEventArgs) -> None:
        with self._when_status_matches_lock:
            futures_and_predicates_dict = self._get_when_status_matches_futures()
            for future in futures_and_predicates_dict:
                predicate = futures_and_predicates_dict[future]
                if not future.done() and predicate(event_args.transfer_status):
                    future.set_result(result=self)
                    self._remove_when_status_matches_future(future=future)

    def get_statistics(self) -> TransferStatistics:
        """
        Calculates transfer statistics for batch transfer

        :return: Calculated statistics of file upload or download for all sessions withing batch transfer
        :rtype: :class:`yellowdog_client.object_store.model.TransferStatistics`
        """
        seed = TransferStatistics.build_new_empty()
        for session in self._transfer_sessions:
            seed += TransferStatistics(
                bytes_transferred=session.bytes_transferred,
                total_bytes=session.file_size,
                elapsed_millis=session.elapsed.microseconds / 1000
            )
        return seed
