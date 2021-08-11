from requests.auth import AuthBase

from .web_requester import WebRequester


class WebRequestFactory(object):
    def __init__(self, auth_base):
        # type: (AuthBase) -> None
        self.__auth_base = auth_base

    def create(self):
        # type: () -> WebRequester
        return WebRequester(auth_base=self.__auth_base)
