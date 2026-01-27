from __future__ import annotations

from abc import ABC, abstractmethod

from yellowdog_client.common import Closeable
from yellowdog_client.model import ApplicationDetails


class ApplicationClient(ABC, Closeable):

    @abstractmethod
    def get_application_details(self) -> ApplicationDetails:
        pass
