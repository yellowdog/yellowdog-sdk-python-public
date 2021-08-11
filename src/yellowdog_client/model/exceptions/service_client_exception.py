from typing import Tuple


class ServiceClientException(Exception):
    __http_status_code = None       # type: int
    __message = None                # type: str
    __details = None                # type: Tuple[str]

    def __init__(self, http_status_code, message, details=()):
        # type: (int, str, Tuple[str]) -> None
        super(ServiceClientException, self).__init__()
        self.__http_status_code = http_status_code
        self.__message = message
        self.__details = details if details is not None else ()

    def __str__(self):
        res = "[HTTP %s] %s" % (
            str(self.__http_status_code),
            self.__message
        )
        if self.__details:
            res = "%s %s" % (res, ", ".join(self.__details))
        return res
