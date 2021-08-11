from typing import Optional
import math


class TransferStatistics(object):
    """
    Calculated file transfer statistics
    """

    bytes_transferred = None                    # type: int
    """
    A number of bytes transferred
    
    :type: int
    """

    total_bytes = None                          # type: int
    """
    A total number of bytes
    
    :type: int
    """

    percentage_transferred = None               # type: float
    """
    Percentage of batch transferred
    
    :type: float
    """

    transfer_speed_bits_per_second = None       # type: int
    """
    Total transfer speed in bits per second
    
    :type: int
    """

    estimated_seconds_remaining = None          # type: int
    """
    Estimated time remaining for transfer to finish
    
    :type: int
    """

    def __init__(self, bytes_transferred=None, total_bytes=None, elapsed_millis=None):
        # type: (Optional[int], Optional[int], Optional[int]) -> None
        self.bytes_transferred = bytes_transferred
        self.total_bytes = total_bytes
        if bytes_transferred is not None and total_bytes is not None and elapsed_millis is not None:
            self.percentage_transferred = self._calculate_percentage_transferred(
                bytes_transferred=bytes_transferred, total_bytes=total_bytes
            )
            self.transfer_speed_bits_per_second = self._calculate_transfer_speed_bits_per_second(
                bytes_transferred=bytes_transferred, elapsed_millis=bytes_transferred
            )
            self.estimated_seconds_remaining = self._estimate_seconds_remaining(
                bytes_transferred=bytes_transferred, total_bytes=total_bytes,
                transfer_speed_bits_per_second=self.transfer_speed_bits_per_second
            )

    @staticmethod
    def _calculate_percentage_transferred(bytes_transferred, total_bytes):
        # type: (int, int) -> float
        if bytes_transferred == 0:
            return 0
        elif bytes_transferred == total_bytes:
            return 100
        else:
            return (100.0 * bytes_transferred) / total_bytes

    @staticmethod
    def _calculate_transfer_speed_bits_per_second(bytes_transferred, elapsed_millis):
        # type: (int, int) -> int
        if elapsed_millis == 0 or bytes_transferred == 0:
            return 0
        else:
            return (bytes_transferred * 8000) / elapsed_millis

    @staticmethod
    def _estimate_seconds_remaining(bytes_transferred, total_bytes, transfer_speed_bits_per_second):
        # type: (int, int, int) -> int
        if transfer_speed_bits_per_second == 0 or bytes_transferred == total_bytes:
            return 0
        else:
            return math.ceil((total_bytes - bytes_transferred) * 8 / transfer_speed_bits_per_second)

    @staticmethod
    def build_new_empty():
        # type: () -> TransferStatistics
        return TransferStatistics(bytes_transferred=0, total_bytes=0, elapsed_millis=0)

    def __add__(self, other):
        # type: (TransferStatistics) -> TransferStatistics
        res = TransferStatistics()
        res.bytes_transferred = self.bytes_transferred + other.bytes_transferred
        res.total_bytes = self.total_bytes + other.total_bytes
        res.percentage_transferred = (self.percentage_transferred + other.percentage_transferred) / 2
        res.transfer_speed_bits_per_second = self.transfer_speed_bits_per_second + other.transfer_speed_bits_per_second
        res.estimated_seconds_remaining = max(self.estimated_seconds_remaining, other.estimated_seconds_remaining)
        return res
