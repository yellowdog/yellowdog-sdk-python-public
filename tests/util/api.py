from http import HTTPStatus

from enum import Enum
from io import BufferedIOBase, BytesIO

from pytest_httpserver import HTTPServer
from typing import Type, TypeVar, Optional, Dict, Union, List, BinaryIO, Iterator
from werkzeug.wrappers import Response

from util.data import make
from yellowdog_client.common.json import Json

from util.sse.event_broadcaster import EventBroadcaster
from util.sse.sse_server import SseServer


class HttpMethod(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"

    def __str__(self) -> str:
        return self.name


T = TypeVar('T')
U = TypeVar('U')


class MockApi:
    def __init__(self, httpserver: HTTPServer):
        self.httpserver = httpserver

    def url(self) -> str:
        return f"http://localhost:{self.httpserver.port}"

    def mock(
            self,
            uri: str,
            method: HttpMethod,
            params: Dict[str, Union[str, List[Optional[str]]]] = None,
            request_type: Optional[Type[U]] = None,
            request: Optional[U] = None,
            response_type: Optional[Type[T]] = None,
            response: Optional[T] = None,
            response_headers: Optional[Dict[str, str]] = None
    ) -> Optional[T]:
        if request_type is not None:
            request = make(request_type)

        data = None
        if request is not None:
            data = Json.dumps(request)

        query_string = None
        if params is not None:
            param_strings = []
            for key, values in params.items():
                if isinstance(values, list):
                    for value in values:
                        param_strings.append(f"{key}={value}")
                else:
                    param_strings.append(f"{key}={values}")

            query_string = "&".join(param_strings)

        request_handler = self.httpserver.expect_oneshot_request(
            uri=uri,
            method=str(method),
            query_string=query_string,
            data=data
        )
        print(f"Expecting: {method} {uri}{'?' if query_string else ''}{query_string}. Body = {data}")

        if response_type is not None:
            response = make(response_type)

        if response is None:
            request_handler.respond_with_response(Response(status=HTTPStatus.OK, headers=response_headers))
        elif isinstance(response, str):
            request_handler.respond_with_data(response, content_type="text/plain", headers=response_headers)
            return response
        elif isinstance(response, bytes):
            request_handler.respond_with_data(response, content_type="application/octet-stream",
                                              headers=response_headers)
            return response
        else:
            request_handler.respond_with_data(Json.dumps(response), content_type="application/json",
                                              headers=response_headers)
            return response

    def mock_stream(self, uri: str, sse_server: SseServer) -> None:
        request_handler = self.httpserver.expect_oneshot_request(
            uri=uri,
            method=str(HttpMethod.GET)
        )
        print(f"Expecting stream: GET {uri}")
        request_handler.respond_with_response(Response(
            status=HTTPStatus.FOUND,
            headers={"Location": sse_server.get_sse_url()}
        ))

    def _generate_stream(self, output_stream: BinaryIO) -> Iterator[bytes]:
        while not output_stream.closed:
            yield output_stream.read(1)

    def verify_all_requests_called(self):
        uncalled_handlers = len(self.httpserver.oneshot_handlers)
        assert uncalled_handlers == 0, f"{uncalled_handlers} requests were not called"
