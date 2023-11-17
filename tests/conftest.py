from http.server import HTTPServer
from textwrap import dedent

import pytest

from util.api import MockApi


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()

    # set a report attribute for each phase of a call, which can
    # be "setup", "call", "teardown"

    setattr(item, "rep_" + rep.when, rep)


@pytest.fixture
def mock_api(httpserver: HTTPServer, request) -> MockApi:
    mock = MockApi(httpserver)
    yield mock
    if request.node.rep_call.failed:
        print()
        print("### Logged Requests ###")
        for request, response in mock.httpserver.log:
            query_string = None if request.query_string == b'' else request.query_string
            data = None if request.data == b'' else request.data

            response_data = None if response.data == b'' else response.data

            print(dedent(f"""\
                      Request: uri='{request.path}' method='{request.method}' query_string={query_string}, data={data}
                      Response: status='{response.status}' body={response_data}
                      """))
        print("### Unhandled Requests ###")
        print(mock.httpserver.format_matchers())

