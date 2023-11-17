from dataclasses import dataclass, asdict
from typing import TypeVar, Type, Dict, Optional

from requests import Request, Session, Response, HTTPError
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from yellowdog_client.model.exceptions import BaseCustomException

from .credentials import ApiKeyAuthenticationHeadersProvider
from .json import Json
from .server_sent_events.sse4python import EventSource

T = TypeVar('T')


class Proxy:
    def __init__(
            self,
            authentication_headers_provider: ApiKeyAuthenticationHeadersProvider,
            retry_count: int,
            max_retry_interval_seconds: int,
            base_url: str = ""
    ) -> None:
        self._authentication_headers_provider: ApiKeyAuthenticationHeadersProvider = authentication_headers_provider
        self._base_url: str = base_url
        self._retry_count: int = retry_count
        self._max_retry_interval_seconds: int = max_retry_interval_seconds

    def append_base_url(self, base_url: str):
        if not base_url:
            raise Exception("Unable to configure client. No base_url has been configured")

        return Proxy(
            self._authentication_headers_provider,
            self._retry_count,
            self._max_retry_interval_seconds,
            self._base_url + base_url
        )

    def get(self, return_type: Type[T], url: str = "", params: Dict[str, object] = None) -> T:
        return self.execute("GET", url, return_type=return_type, params=params)

    def put(self, return_type: Type[T] = None, data: object = None, url: str = "") -> T:
        return self.execute("PUT", url, data, return_type)

    def post(self, return_type: Type[T] = None, data: object = None, url: str = "",
             params: Dict[str, object] = None) -> T:
        return self.execute("POST", url, data, return_type, params)

    def delete(self, url: str = "", return_type: Type[T] = None) -> T:
        return self.execute("DELETE", url, return_type=return_type)

    def execute(self, method: str, url: str = "", data: object = None, return_type: Type[T] = None,
                params: Dict[str, object] = None) -> T:
        response = self.raw_execute(method, url, Json.dump(data) if data else None, params)
        return Json.load(response.json(), return_type) if return_type else None

    def raw_execute(self, method: str, url: str = "", json: object = None, params: Dict[str, object] = None):
        return self.execute_session_with_retries(
            request=Request(
                method=method,
                url=self._base_url + url,
                auth=self._authentication_headers_provider,
                json=json,
                params=params
            ),
            prefix_url=self._base_url,
            retry_count=self._retry_count,
            max_retry_interval_seconds=self._max_retry_interval_seconds
        )

    def stream(self, url: str = "") -> EventSource:
        return EventSource(
            url=self._base_url + url,
            auth=self._authentication_headers_provider
        )

    def execute_with_timeout(self, method: str, timeout: int, url: str = "", data: object = None,
                             headers: Dict[str, str] = None) -> Response:
        request = Request(
            method=method,
            auth=self._authentication_headers_provider,
            url=self._base_url + url,
            headers=headers,
            data=data
        )

        session = Session()
        prepared_request = session.prepare_request(request)
        settings = session.merge_environment_settings(prepared_request.url, {}, None, None, None)
        response = session.send(request=prepared_request, timeout=timeout, **settings)
        return self._handle_response(response)

    @classmethod
    def execute_session_with_retries(
            cls,
            request: Request,
            prefix_url: str,
            retry_count: int,
            max_retry_interval_seconds: int
    ) -> Response:
        session = Session()
        prepared_request = session.prepare_request(request)
        settings = session.merge_environment_settings(prepared_request.url, {}, None, None, None)
        session.mount(
            prefix=prefix_url,
            adapter=HTTPAdapter(max_retries=Retry(
                total=retry_count,
                backoff_factor=2,
                # Not available until urllib3 2.0.0
                # backoff_jitter=0.5,
                # Not available until urllib3 2.0.0
                # backoff_max=max_retry_interval_seconds,
                # Override the default to include POST
                allowed_methods=frozenset(['GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'OPTIONS', 'TRACE']),
                # Explicitly list all the status codes that we want to retry on because the default list is both not
                # want we want and only applies if the server responds with a Retry-After header
                status_forcelist=[500, 501, 502, 503, 504, 505, 506, 507, 508, 509, 510, 511],
                # Don't raise an error as this is already handled below
                raise_on_status=False
            ))
        )

        response = session.send(request=prepared_request, **settings)
        return cls._handle_response(response)

    @staticmethod
    def to_params(*args: dataclass) -> dict:
        params = {}

        for arg in args:
            raw_dict = asdict(arg)
            for key in raw_dict.keys():
                value = raw_dict[key]
                if isinstance(value, dict):
                    for nested_key in value.keys():
                        params[key + "." + nested_key] = value[nested_key]
                elif value is not None:
                    params[key] = value

        return params

    @classmethod
    def _handle_response(cls, response: Response) -> Response:
        if not response.ok:
            custom_exception = cls._try_convert_to_file_transfer_exception(response)
            if custom_exception:
                raise custom_exception
            else:
                cls._raise_for_status(response)
        return response

    @staticmethod
    def _try_convert_to_file_transfer_exception(response: Response) -> Optional[Exception]:
        if not response.text:
            return None

        # noinspection PyBroadException
        try:
            res = Json.loads(response.text, BaseCustomException)
        except Exception:
            # If conversion fails, we return None so that normal exception handling can resume
            return None

        # If the conversion succeeds, but we don't have an error type, then the lenient deserialization has
        # allowed the conversion, but it isn't really a custom exception so handle it as normal
        if not hasattr(res, "errorType"):
            return None

        return res

    @staticmethod
    def _raise_for_status(response: Response, max_text_length=500):
        """Raises stored :class:`HTTPError`, if one occurred."""

        http_error_msg = ''
        if isinstance(response.reason, bytes):
            try:
                reason = response.reason.decode('utf-8')
            except UnicodeDecodeError:
                reason = response.reason.decode('iso-8859-1')
        else:
            reason = response.reason

        if 400 <= response.status_code < 500:
            http_error_msg = u'%s Client Error: %s for url: %s' % (response.status_code, reason, response.url)

        elif 500 <= response.status_code < 600:
            http_error_msg = u'%s Server Error: %s for url: %s' % (response.status_code, reason, response.url)

        if http_error_msg:
            http_error_msg += u' Response Body: %s' % response.text[:max_text_length]
        raise HTTPError(http_error_msg, response=response)
