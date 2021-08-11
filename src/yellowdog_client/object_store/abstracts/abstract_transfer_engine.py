from queue import Queue
from typing import List
from threading import Event
import time

from .abstract_object_store_service_proxy import AbstractObjectStoreServiceProxy as Proxy
from .abstract_notification_dispatcher import AbstractNotificationDispatcher as NotificationDispatcher
from .abstract_session import AbstractSession
from yellowdog_client.object_store.model import FileTransferStatus
from yellowdog_client.object_store.utils.background_thread_factory import BackgroundThreadFactory as ThreadFactory
from yellowdog_client.object_store.utils.background_thread import BackgroundThread
from yellowdog_client.object_store.utils.chunk_transfer_throttle import ChunkTransferThrottle as Throttle
from .abstract_chunk_transfer_task import AbstractChunkTransferTask


class AbstractTransferEngine(object):
    THREAD_TASK_MULTIPLIER = 5                      # type: int
    TRANSFER_THREAD_STOP_WAIT_S = 0.1               # type: float
    DEFAULT_CHUNK_SIZE = 1024 * 512                 # type: int     # transfer in 512KB chunks
    DEFAULT_FILE_RETRY_COUNT = 3                    # type: int     # retry file transfer 3 times (4 attempts in total)

    @property
    def chunk_size(self):
        # type: () -> int
        return self._chunk_size

    @chunk_size.setter
    def chunk_size(self, value):
        # type: (int) -> None
        self._chunk_size = value

    @property
    def file_retry_count(self):
        # type: () -> int
        return self._file_retry_count

    @file_retry_count.setter
    def file_retry_count(self, value):
        # type: (int) -> None
        self._file_retry_count = value

    @property
    def max_bytes_per_second(self):
        # type: () -> int
        return self._transfer_throttle.max_bytes_per_second

    @max_bytes_per_second.setter
    def max_bytes_per_second(self, value):
        # type: (int) -> None
        self._transfer_throttle.max_bytes_per_second = value

    @property
    def active_sessions(self):
        # type: () -> List[AbstractSession]
        return [x for x in self._sessions if x.status.is_active()]

    @property
    def all_sessions(self):
        # type: () -> List[AbstractSession]
        return [x for x in self._sessions]

    @property
    def transfer_threads_alive(self):
        # type: () -> bool
        return any([x for x in self._transfer_threads if x.is_alive()])

    def __init__(self, service_proxy, thread_factory, notification_dispatcher, chunk_transfer_throttle,
                 transfer_thread_count):
        # type: (Proxy, ThreadFactory, NotificationDispatcher, Throttle, int) -> None
        if transfer_thread_count <= 0:
            raise ValueError("transfer_thread_count must be greater than 0")

        self._service_proxy = service_proxy                         # type: Proxy
        self._thread_factory = thread_factory                       # type: ThreadFactory
        self._notification_dispatcher = notification_dispatcher     # type: NotificationDispatcher
        self._chunk_task_queue = Queue(maxsize=transfer_thread_count * self.THREAD_TASK_MULTIPLIER)     # type: Queue
        self._transfer_thread_count = transfer_thread_count         # type: int
        self._transferring = Event()                                # type: Event
        self._transfer_throttle = chunk_transfer_throttle           # type: Throttle
        self._chunk_size = self.DEFAULT_CHUNK_SIZE                  # type: int
        self._file_retry_count = self.DEFAULT_FILE_RETRY_COUNT      # type: int
        self._sessions = []                                         # type: List[AbstractSession]

        # now that thread controls are initialised we can create our own thread pool
        self._transfer_threads = self._create_transfer_threads()    # type: List[BackgroundThread]

    def _create_transfer_threads(self):
        # type: () -> List[BackgroundThread]
        transfer_threads = []
        for _ in range(0, self._transfer_thread_count):
            thread = self._thread_factory.new_thread(target=self._process_chunk_tasks)
            transfer_threads.append(thread)
            thread.start()
        return transfer_threads

    def _process_chunk_tasks(self):
        # type: () -> None
        while True:
            try:
                self._transferring.wait()
                task = self._chunk_task_queue.get()
                self._synchronised_chunk_transfer(task=task)
            except Exception as ex:
                print("Unexpected error occurred while processing chunk task %s" % str(ex))

    def _synchronised_chunk_transfer(self, task):
        # type: (AbstractChunkTransferTask) -> None
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

    def _transfer_chunk(self, chunk_transfer_task, chunk_hash):
        # type: (AbstractChunkTransferTask, str) -> str
        raise NotImplementedError("Needs implementation")

    def _add_session(self, session):
        # type: (AbstractSession) -> None
        self._sessions.append(session)

    def stop_transfers(self):
        # type: () -> None
        self._transferring.clear()
        self._transfer_throttle.stop()
        while self.transfer_threads_alive:
            time.sleep(self.TRANSFER_THREAD_STOP_WAIT_S)

    def start_transfers(self):
        # type: () -> None
        self._transfer_throttle.start()
        self._transferring.set()
        [x.start() for x in self._sessions if x.status == FileTransferStatus.Ready]

    def enqueue_chunk_transfer_task(self, chunk_task):
        # type: (AbstractChunkTransferTask) -> None
        if chunk_task is None:
            raise ValueError("chunk_task cannot be null")

        self._chunk_task_queue.put(chunk_task)

    def clear_inactive_sessions(self):
        # type: () -> None
        self._sessions = [x for x in self._sessions if not x.status.is_active()]

    def abort_all_transfers(self):
        # type: () -> None
        [x.abort() for x in self.active_sessions]
