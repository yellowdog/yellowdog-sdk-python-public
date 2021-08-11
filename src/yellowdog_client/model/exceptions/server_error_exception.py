from typing import Tuple

from .service_client_exception import ServiceClientException


class ServerErrorException(ServiceClientException):
    def __init__(self, http_status_code, message, details=()):
        # type: (int, str, Tuple[str]) -> None
        super(ServerErrorException, self).__init__(
            http_status_code=http_status_code,
            message=message,
            details=details
        )

    @staticmethod
    def create_subscription_cancelled_error():
        # type: () -> ServerErrorException
        return ServerErrorException(
            http_status_code=204,
            message="Server has cancelled subscription",
            details=tuple()
        )
