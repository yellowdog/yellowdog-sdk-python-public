from typing import List, TypeVar

from .common import Closeable

T = TypeVar('T', bound=Closeable)


class ClientCollection(Closeable):
    def __init__(self) -> None:
        self.__clients: List[Closeable] = []

    def add(self, client: T) -> T:
        self.__clients.append(client)
        return client

    def close(self) -> None:
        for client in self.__clients:
            client.close()
