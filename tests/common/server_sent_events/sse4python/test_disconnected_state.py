from .callback_fixture import CallbackFixture
from yellowdog_client.common.server_sent_events.sse4python import DisconnectedState
import pytest


class TestDisconnectedState(CallbackFixture):
    def test__no_url__expect_value_error(self, mocker):
        with pytest.raises(ValueError):
            DisconnectedState(url=None, web_requester_factory=mocker.MagicMock())

    def test_run__cancelled__expect_disconnected_thread_started_following_with_callback(self, mocker,
                                                                                        thread_callback_init):
        callback = thread_callback_init
        cancel_token = mocker.MagicMock()
        cancel_token.cancelled = True

        state = DisconnectedState(url="URL", web_requester_factory=mocker.MagicMock())
        thread = state.run(
            message_received=mocker.MagicMock(),
            error_handle=mocker.MagicMock(),
            completed=mocker.MagicMock(),
            cancel_token=cancel_token,
            continuation_callback=callback
        )
        thread.join()

        assert self._callback_executed
        assert type(self._thread_result) == DisconnectedState
        assert id(self._thread_result) != id(state)

    def test_run__non_cancelled__expect_connecting_thread_started_following_with_callback(self, mocker,
                                                                                          thread_callback_init):
        callback = thread_callback_init
        cancel_token = mocker.MagicMock()
        cancel_token.cancelled = False
        mock_connecting = mocker.patch(
            "yellowdog_client.common.server_sent_events.sse4python.connecting_state.ConnectingState"
        )
        web_request_factory = mocker.MagicMock()

        state = DisconnectedState(url="URL", web_requester_factory=web_request_factory)
        thread = state.run(
            message_received=mocker.MagicMock(),
            error_handle=mocker.MagicMock(),
            completed=mocker.MagicMock(),
            cancel_token=cancel_token,
            continuation_callback=callback
        )
        thread.join()

        assert self._callback_executed
        assert self._thread_result == mock_connecting.return_value
        mock_connecting.assert_called_once_with(url="URL", web_requester_factory=web_request_factory)
