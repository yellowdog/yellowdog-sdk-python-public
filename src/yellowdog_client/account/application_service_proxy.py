from yellowdog_client.common import Proxy
from yellowdog_client.model import ApplicationDetails


class ApplicationServiceProxy:
    def __init__(self, proxy: Proxy) -> None:
        self.proxy: Proxy = proxy.append_base_url("/application/")

    def get_application_details(self) -> ApplicationDetails:
        return self.proxy.get(ApplicationDetails)

