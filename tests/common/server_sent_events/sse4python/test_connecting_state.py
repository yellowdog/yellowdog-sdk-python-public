from .callback_fixture import CallbackFixture
from yellowdog_client.common.server_sent_events.sse4python import ConnectingState
import pytest


class TestConnectingState(CallbackFixture):
    def test__no_url__expect_value_error(self, mocker):
        with pytest.raises(ValueError):
            ConnectingState(url=None, web_requester_factory=mocker.MagicMock())

    def test__no_factory__expect_value_error(self):
        with pytest.raises(ValueError):
            ConnectingState(url="URL", web_requester_factory=None)

    @staticmethod
    def mock_requester_get(url, callback):
        assert url == "URL"
        return callback("RESPONSE")

    @pytest.fixture
    def mock_web_request_factory_executing_callbacks(self, mocker):
        mock_requester = mocker.MagicMock()
        mock_requester.get = self.mock_requester_get
        mock_factory = mocker.MagicMock()
        mock_factory.create.return_value = mock_requester
        return mock_factory

    def test_run__cancelled__expect_disconnected_thread_started_followed_with_callback(self, mocker,
                       thread_callback_init, mock_web_request_factory_executing_callbacks):
        callback = thread_callback_init
        cancel_token = mocker.MagicMock()
        cancel_token.cancelled = True
        mock_disconnected = mocker.patch(
            "yellowdog_client.common.server_sent_events.sse4python.disconnected_state.DisconnectedState"
        )

        state = ConnectingState(url="URL", web_requester_factory=mock_web_request_factory_executing_callbacks)
        thread = state.run(
            message_received=mocker.MagicMock(),
            error_handle=mocker.MagicMock(),
            completed=mocker.MagicMock(),
            cancel_token=cancel_token,
            continuation_callback=callback
        )
        thread.join()

        assert self._callback_executed
        assert self._thread_result == mock_disconnected.return_value
        mock_disconnected.assert_called_once_with(
            url="URL",
            web_requester_factory=mock_web_request_factory_executing_callbacks
        )

    def test_run__non_cancelled__expect_connected_thread_started_with_response_followed_with_callback(self, mocker,
                                   thread_callback_init, mock_web_request_factory_executing_callbacks):
        callback = thread_callback_init
        cancel_token = mocker.MagicMock()
        cancel_token.cancelled = False
        mock_connected = mocker.patch(
            "yellowdog_client.common.server_sent_events.sse4python.connected_state.ConnectedState"
        )

        state = ConnectingState(url="URL", web_requester_factory=mock_web_request_factory_executing_callbacks)
        thread = state.run(
            message_received=mocker.MagicMock(),
            error_handle=mocker.MagicMock(),
            completed=mocker.MagicMock(),
            cancel_token=cancel_token,
            continuation_callback=callback
        )
        thread.join()

        assert self._callback_executed
        assert self._thread_result == mock_connected.return_value
        mock_connected.assert_called_once_with(
            url="URL", response="RESPONSE", web_requester_factory=mock_web_request_factory_executing_callbacks
        )
