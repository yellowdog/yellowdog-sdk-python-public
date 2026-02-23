from typing import Tuple, Optional


class ServiceClientException(Exception):
    __http_status_code: Optional[int] = None
    __message: Optional[str] = None
    __details: Optional[Tuple[str, ...]] = None

    def __init__(self, http_status_code: int, message: str, details: Tuple[str, ...] = ()) -> None:
        super().__init__()
        self.__http_status_code = http_status_code
        self.__message = message
        self.__details = details if details is not None else ()

    def __str__(self) -> str:
        res = "[HTTP %s] %s" % (
            str(self.__http_status_code),
            self.__message
        )
        if self.__details:
            res = "%s %s" % (res, ", ".join(self.__details))
        return res
