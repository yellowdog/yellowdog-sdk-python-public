from typing import Callable, Optional
import time
import os
import shutil


class TimeoutException(Exception):
    pass


class FileUtils(object):
    DEFAULT_FILE_WAIT_TIMEOUT_MS: int = 5000

    @staticmethod
    def with_retry(action: Callable, timeout_ms: Optional[int] = None) -> None:
        if timeout_ms is None:
            timeout_ms = FileUtils.DEFAULT_FILE_WAIT_TIMEOUT_MS
        start_time_ms = time.time() * 1000
        while (time.time() * 1000) - start_time_ms < timeout_ms:
            try:
                action()
                return
            except IOError:
                # Do nothing. Maybe file is being used at the moment
                print("Could not rename a file. File may be in use by another process. Retrying")

        raise TimeoutException("Failed to perform action within allotted time.")

    @staticmethod
    def rename_replace(source_file_path: str, destination_file_path: str) -> None:
        if os.path.isfile(destination_file_path):
            os.remove(destination_file_path)
        FileUtils.with_retry(action=lambda: shutil.move(source_file_path, destination_file_path))
