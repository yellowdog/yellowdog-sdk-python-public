from yellowdog_client.common.server_sent_events.sse4python import WebRequestFactory


class TestCreate(object):
    def test__expect_requester_returned_with_headers_passed(self, mocker):
        mock_requester = mocker.patch(
            "yellowdog_client.common.server_sent_events.sse4python.web_request_factory.WebRequester"
        )
        auth_base = mocker.MagicMock()

        factory = WebRequestFactory(auth_base=auth_base)

        res = factory.create()

        assert res == mock_requester.return_value
        mock_requester.assert_called_once_with(auth_base=auth_base)
