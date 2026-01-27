from yellowdog_client.account.application_client import ApplicationClient
from yellowdog_client.account.application_service_proxy import ApplicationServiceProxy
from yellowdog_client.model import ApplicationDetails


class ApplicationClientImpl(ApplicationClient):
    def __init__(self, service_proxy: ApplicationServiceProxy) -> None:
        self.__service_proxy = service_proxy

    def get_application_details(self) -> ApplicationDetails:
        return self.__service_proxy.get_application_details()

    def close(self) -> None:
        pass

