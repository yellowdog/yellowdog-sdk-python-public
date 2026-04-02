import gzip
import json as json_module
from dataclasses import asdict
from datetime import datetime, timedelta
from typing import TypeVar, Type, Dict, Optional, overload, Any

from requests import Request, Session, Response, HTTPError

from yellowdog_client.model.exceptions import BaseCustomException
from .credentials import ApiKeyAuthenticationHeadersProvider
from .iso_datetime import iso_timedelta_format, iso_format
from .json import Json
from .server_sent_events.sse4python import EventSource
from .user_agent import UserAgent

T = TypeVar('T')


class Proxy:
    GZIP_THRESHOLD_BYTES = 2048

    def __init__(
            self,
            authentication_headers_provider: ApiKeyAuthenticationHeadersProvider,
            session: Session,
            user_agent: UserAgent,
            base_url: str = "",
            compress_requests: bool = False
    ) -> None:
        self._authentication_headers_provider: ApiKeyAuthenticationHeadersProvider = authentication_headers_provider
        self._user_agent: UserAgent = user_agent
        self._base_url: str = base_url
        self._compress_requests: bool = compress_requests
        self._session: Session = session

    @staticmethod
    def _format_params(params: Optional[Dict[str, object]]) -> None:
        if params is not None:
            for key, value in params.items():
                if isinstance(value, datetime):
                    params[key] = iso_format(value)
                elif isinstance(value, timedelta):
                    params[key] = iso_timedelta_format(value)

    def append_base_url(self, base_url: Optional[str]) -> 'Proxy':
        if not base_url:
            raise Exception("Unable to configure client. No base_url has been configured")

        return Proxy(
            self._authentication_headers_provider,
            self._session,
            self._user_agent,
            self._base_url + base_url,
            self._compress_requests
        )

    def get(self, return_type: Type[T], url: str = "", params: Optional[Dict[str, Any]] = None) -> T:
        return self.execute("GET", url, return_type=return_type, params=params)

    @overload
    def put(self, return_type: None = None, data: Optional[object] = None, url: str = "") -> None:
        ...

    @overload
    def put(self, return_type: Type[T], data: Optional[object] = None, url: str = "") -> T:
        ...

    def put(self, return_type: Optional[Type[T]] = None, data: Optional[object] = None, url: str = "") -> Optional[T]:
        return self.execute("PUT", url, data, return_type)

    @overload
    def post(self, return_type: None = None, data: Optional[object] = None, url: str = "",
             params: Optional[Dict[str, object]] = None) -> None:
        ...

    @overload
    def post(self, return_type: Type[T], data: Optional[object] = None, url: str = "",
             params: Optional[Dict[str, object]] = None) -> T:
        ...

    def post(self, return_type: Optional[Type[T]] = None, data: Optional[object] = None, url: str = "",
             params: Optional[Dict[str, object]] = None) -> Optional[T]:
        return self.execute("POST", url, data, return_type, params)

    @overload
    def delete(self, url: str = "", return_type: None = None) -> None:
        ...

    @overload
    def delete(self, url: str = "", return_type: Type[T] = ...) -> T:
        ...

    def delete(self, url: str = "", return_type: Optional[Type[T]] = None) -> Optional[T]:
        return self.execute("DELETE", url, return_type=return_type)

    @overload
    def execute(self, method: str, url: str = "", data: Optional[object] = None, return_type: None = None,
                params: Optional[Dict[str, object]] = None) -> None:
        ...

    @overload
    def execute(self, method: str, url: str = "", data: Optional[object] = None, return_type: Type[T] = ...,
                params: Optional[Dict[str, object]] = None) -> T:
        ...

    def execute(self, method: str, url: str = "", data: Optional[object] = None, return_type: Optional[Type[T]] = None,
                params: Optional[Dict[str, object]] = None) -> Optional[T]:
        self._format_params(params)
        response = self.raw_execute(method, url, Json.dump(data) if data else None, params)
        return Json.load(response.json(), return_type) if return_type else None

    def raw_execute(self, method: str, url: str = "", json: Optional[object] = None, params: Optional[Dict[str, object]] = None) -> Response:
        headers = self._get_user_agent_headers()

        if self._compress_requests and json is not None:
            body_bytes = json_module.dumps(json).encode("utf-8")
            if len(body_bytes) > self.GZIP_THRESHOLD_BYTES:
                headers["Content-Encoding"] = "gzip"
                headers["Content-Type"] = "application/json"
                request_kwargs: Dict[str, Any] = dict(data=gzip.compress(body_bytes))
            else:
                request_kwargs = dict(json=json)
        else:
            request_kwargs = dict(json=json)

        request = Request(
            method=method,
            url=self._base_url + url,
            auth=self._authentication_headers_provider,
            params=params,
            headers=headers,
            **request_kwargs
        )
        prepared_request = self._session.prepare_request(request)
        settings = self._session.merge_environment_settings(prepared_request.url, {}, None, None, None)
        response = self._session.send(request=prepared_request, **settings)
        return self._handle_response(response)

    def stream(self, url: str = "") -> EventSource:
        return EventSource(
            url=self._base_url + url,
            auth=self._authentication_headers_provider,
            headers=self._get_user_agent_headers()
        )

    def execute_with_timeout(self, method: str, timeout: int, url: str = "", data: Optional[object] = None,
                             additional_headers: Optional[Dict[str, str]] = None) -> Response:

        headers = self._get_user_agent_headers()
        if additional_headers:
            headers.update(additional_headers)

        request = Request(
            method=method,
            auth=self._authentication_headers_provider,
            url=self._base_url + url,
            headers=headers,
            data=data
        )

        prepared_request = self._session.prepare_request(request)
        settings = self._session.merge_environment_settings(prepared_request.url, {}, None, None, None)
        response = self._session.send(request=prepared_request, timeout=timeout, **settings)
        return self._handle_response(response)

    @staticmethod
    def to_params(*args: Any) -> Dict[str, str]:
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
    def _raise_for_status(response: Response, max_text_length: int = 500) -> None:
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

    def _get_user_agent_headers(self) -> Dict[str, str]:
        return {
            "User-Agent": f"yd/1.0.0"
                          f" {self._user_agent.application_id}/{self._user_agent.application_version}"
                          f" python/{self._user_agent.python_version}"
        }
