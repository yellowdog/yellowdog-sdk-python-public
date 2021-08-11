from yellowdog_client.common.server_sent_events.sse4python import ServerResponse


class TestServerResponse(object):
    def test__yield_session_events__10_values__cancels_after_5_values__expect_only_5_values_returned(self, mocker):
        cancel_token = mocker.MagicMock()
        cancelled = mocker.PropertyMock(side_effect=[False, False, False, False, False, True])
        type(cancel_token).cancelled = cancelled

        response = ServerResponse(sse_session=["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"])
        res = [x for x in response.yield_session_events(cancel_token=cancel_token)]

        assert res == ["a", "b", "c", "d", "e"]
