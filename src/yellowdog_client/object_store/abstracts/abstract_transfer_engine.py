import traceback
from queue import Queue
from threading import Event
from typing import List

import time

from yellowdog_client.object_store.model import FileTransferStatus
from yellowdog_client.object_store.utils.background_thread import BackgroundThread
from yellowdog_client.object_store.utils.background_thread_factory import BackgroundThreadFactory as ThreadFactory
from yellowdog_client.object_store.utils.chunk_transfer_throttle import ChunkTransferThrottle as Throttle
from .abstract_chunk_transfer_task import AbstractChunkTransferTask
from .abstract_notification_dispatcher import AbstractNotificationDispatcher as NotificationDispatcher
from .abstract_object_store_service_proxy import AbstractObjectStoreServiceProxy as Proxy
from .abstract_session import AbstractSession


class AbstractTransferEngine(object):
    THREAD_TASK_MULTIPLIER: int = 5
    TRANSFER_THREAD_STOP_WAIT_S: float = 0.1
    DEFAULT_CHUNK_SIZE: int = 5242880  # 5MB
    DEFAULT_FILE_RETRY_COUNT: int = 3  # retry file transfer 3 times (4 attempts in total)

    @property
    def chunk_size(self) -> int:
        return self._chunk_size

    @chunk_size.setter
    def chunk_size(self, value: int) -> None:
        self._chunk_size = value

    @property
    def file_retry_count(self) -> int:
        return self._file_retry_count

    @file_retry_count.setter
    def file_retry_count(self, value: int) -> None:
        self._file_retry_count = value

    @property
    def max_bytes_per_second(self) -> int:
        return self._transfer_throttle.max_bytes_per_second

    @max_bytes_per_second.setter
    def max_bytes_per_second(self, value: int) -> None:
        self._transfer_throttle.max_bytes_per_second = value

    @property
    def active_sessions(self) -> List[AbstractSession]:
        return [x for x in self._sessions if x.status.is_active()]

    @property
    def all_sessions(self) -> List[AbstractSession]:
        return [x for x in self._sessions]

    @property
    def transfer_threads_alive(self) -> bool:
        return any([x for x in self._transfer_threads if x.is_alive()])

    def __init__(
            self,
            service_proxy: Proxy,
            thread_factory: ThreadFactory,
            notification_dispatcher: NotificationDispatcher,
            chunk_transfer_throttle: Throttle,
            transfer_thread_count: int
    ) -> None:
        if transfer_thread_count <= 0:
            raise ValueError("transfer_thread_count must be greater than 0")

        self._service_proxy: Proxy = service_proxy
        self._thread_factory: ThreadFactory = thread_factory
        self._notification_dispatcher: NotificationDispatcher = notification_dispatcher
        self._chunk_task_queue: Queue = Queue(maxsize=transfer_thread_count * self.THREAD_TASK_MULTIPLIER)
        self._transfer_thread_count: int = transfer_thread_count
        self._transferring: Event = Event()
        self._transfer_throttle: Throttle = chunk_transfer_throttle
        self._chunk_size: int = self.DEFAULT_CHUNK_SIZE
        self._file_retry_count: int = self.DEFAULT_FILE_RETRY_COUNT
        self._sessions: List[AbstractSession] = []

        # now that thread controls are initialised we can create our own thread pool
        self._transfer_threads: List[BackgroundThread] = self._create_transfer_threads()

    def _create_transfer_threads(self) -> List[BackgroundThread]:
        transfer_threads = []
        for _ in range(0, self._transfer_thread_count):
            thread = self._thread_factory.new_thread(target=self._process_chunk_tasks)
            transfer_threads.append(thread)
            thread.start()
        return transfer_threads

    def _process_chunk_tasks(self) -> None:
        while True:
            try:
                self._transferring.wait()
                task = self._chunk_task_queue.get()
                self._synchronised_chunk_transfer(task=task)
            except Exception as ex:
                print("Unexpected error occurred while processing chunk task %s" % str(ex))
                print(traceback.format_exc())

    def _synchronised_chunk_transfer(self, task: AbstractChunkTransferTask) -> None:
        self._transfer_throttle.wait_for_transfer_bandwidth(
            chunk_size=task.chunk_size, cancellation_token=task.abort_token
        )

        if task.abort_token.cancelled:
            return

        try:
            chunk_hash = self._transfer_chunk(chunk_transfer_task=task, chunk_hash="")
            task.notify_chunk_transferred(chunk_hash)
        except Exception as ex_any:
            task.notify_exception(ex_any)
        finally:
            task.transfer_countdown.counter -= 1

    def _transfer_chunk(self, chunk_transfer_task: AbstractChunkTransferTask, chunk_hash: str) -> str:
        raise NotImplementedError("Needs implementation")

    def _add_session(self, session: AbstractSession) -> None:
        self._sessions.append(session)

    def stop_transfers(self) -> None:
        self._transferring.clear()
        self._transfer_throttle.stop()
        while self.transfer_threads_alive:
            time.sleep(self.TRANSFER_THREAD_STOP_WAIT_S)

    def start_transfers(self) -> None:
        self._transfer_throttle.start()
        self._transferring.set()
        [x.start() for x in self._sessions if x.status == FileTransferStatus.Ready]

    def enqueue_chunk_transfer_task(self, chunk_task: AbstractChunkTransferTask) -> None:
        if chunk_task is None:
            raise ValueError("chunk_task cannot be null")

        self._chunk_task_queue.put(chunk_task)

    def clear_inactive_sessions(self) -> None:
        self._sessions = [x for x in self._sessions if not x.status.is_active()]

    def abort_all_transfers(self) -> None:
        [x.abort() for x in self.active_sessions]
