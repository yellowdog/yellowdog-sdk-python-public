from .callback_fixture import CallbackFixture
from yellowdog_client.common.server_sent_events.sse4python import ConnectedState
from yellowdog_client.common.server_sent_events.sse4python import ServerSentEvent
import pytest
from collections import namedtuple

Event = namedtuple('Event', ['data', 'event', 'id', 'retry'])
Random = namedtuple('Random', ['foo', 'bar'])


class TestConnectedState(CallbackFixture):
    def message_callback(self, response):
        self._message_callback_executed = True
        self._message_callback_result.append(response)

    @pytest.fixture
    def message_callback_init(self):
        self._message_callback_executed = False
        self._message_callback_result = []
        return self.message_callback

    def completed_callback(self):
        self._completed_callback_executed = True

    @pytest.fixture
    def completed_callback_init(self):
        self._completed_callback_executed = False
        return self.completed_callback

    def error_callback(self, error):
        self._error_callback_executed = True
        self._error_callback_results.append(error)

    @pytest.fixture
    def error_callback_init(self):
        self._error_callback_executed = False
        self._error_callback_results = []
        return self.error_callback

    @pytest.fixture
    def mock_response_error(self, mocker):
        response = mocker.MagicMock()
        response.yield_session_events.side_effect = Exception("TESTING")
        return response

    @pytest.fixture
    def mock_response_empty(self, mocker):
        response = mocker.MagicMock()
        response.yield_session_events.return_value = []
        return response

    @pytest.fixture
    def mock_response_unknown_objects(self, mocker):
        response = mocker.MagicMock()
        response.yield_session_events.return_value = [
            Random("foo1", "bar1"),
            Random("foo2", "bar2"),
            Random("foo3", "bar3")
        ]
        return response

    @pytest.fixture
    def mock_response_full(self, mocker):
        response = mocker.MagicMock()
        response.yield_session_events.return_value = [
            Event("DATA1", "EVENT1", "ID1", 1),
            Event("DATA2", "EVENT2", "ID2", 2),
            Event("DATA3", "EVENT3", "ID3", 3)
        ]
        return response

    def test__run__cancelled__expect_complete_invoked__disconnect_returned__followed_by_callback(self, mocker,
            thread_callback_init, message_callback_init, error_callback_init, completed_callback_init,
            mock_response_full):
        thread_callback = thread_callback_init
        message_callback = message_callback_init
        error_callback = error_callback_init
        completed_callback = completed_callback_init

        mock_web_factory = mocker.MagicMock()
        cancel_token = mocker.MagicMock()
        cancel_token.cancelled = True
        mock_disconnected = mocker.patch(
            "yellowdog_client.common.server_sent_events.sse4python.disconnected_state.DisconnectedState"
        )

        state = ConnectedState(url="URL", response=mock_response_full, web_requester_factory=mock_web_factory)
        thread = state.run(
            message_received=message_callback,
            error_handle=error_callback,
            completed=completed_callback,
            cancel_token=cancel_token,
            continuation_callback=thread_callback
        )
        thread.join()

        assert self._callback_executed
        assert self._thread_result == mock_disconnected.return_value
        mock_disconnected.assert_called_once_with(
            url="URL", web_requester_factory=mock_web_factory
        )
        assert not self._message_callback_executed
        assert not self._error_callback_executed
        assert self._completed_callback_executed

    def test__run__non_cancelled__error_raised__expect_complete_and_error_invoked__disconnect_returned__followed_by_callback(
            self, mocker, thread_callback_init, message_callback_init, error_callback_init, completed_callback_init,
            mock_response_error):
        thread_callback = thread_callback_init
        message_callback = message_callback_init
        error_callback = error_callback_init
        completed_callback = completed_callback_init

        mock_web_factory = mocker.MagicMock()
        cancel_token = mocker.MagicMock()
        cancel_token.cancelled = False
        mock_disconnected = mocker.patch(
            "yellowdog_client.common.server_sent_events.sse4python.disconnected_state.DisconnectedState"
        )

        state = ConnectedState(url="URL", response=mock_response_error, web_requester_factory=mock_web_factory)
        thread = state.run(
            message_received=message_callback,
            error_handle=error_callback,
            completed=completed_callback,
            cancel_token=cancel_token,
            continuation_callback=thread_callback
        )
        thread.join()

        assert self._callback_executed
        assert self._thread_result == mock_disconnected.return_value
        mock_disconnected.assert_called_once_with(
            url="URL", web_requester_factory=mock_web_factory
        )
        assert not self._message_callback_executed
        assert self._error_callback_executed
        assert type(self._error_callback_results[0]) == Exception
        assert str(self._error_callback_results[0]) == "TESTING"
        assert self._completed_callback_executed

    def test__run__non_cancelled__empty_events__expect_complete_invoked__disconnect_returned__followed_by_callback(
            self, mocker, thread_callback_init, message_callback_init, error_callback_init, completed_callback_init,
            mock_response_empty):
        thread_callback = thread_callback_init
        message_callback = message_callback_init
        error_callback = error_callback_init
        completed_callback = completed_callback_init

        mock_web_factory = mocker.MagicMock()
        cancel_token = mocker.MagicMock()
        cancel_token.cancelled = False
        mock_disconnected = mocker.patch(
            "yellowdog_client.common.server_sent_events.sse4python.disconnected_state.DisconnectedState"
        )

        state = ConnectedState(url="URL", response=mock_response_empty, web_requester_factory=mock_web_factory)
        thread = state.run(
            message_received=message_callback,
            error_handle=error_callback,
            completed=completed_callback,
            cancel_token=cancel_token,
            continuation_callback=thread_callback
        )
        thread.join()

        assert self._callback_executed
        assert self._thread_result == mock_disconnected.return_value
        mock_disconnected.assert_called_once_with(
            url="URL", web_requester_factory=mock_web_factory
        )
        assert not self._message_callback_executed
        assert not self._error_callback_executed
        assert self._completed_callback_executed

    def test__run__non_cancelled__unknown_events__expect_message_invoked_with_none_values__complete_invoked__disconnect_returned__followed_by_callback(
            self, mocker, thread_callback_init, message_callback_init, error_callback_init, completed_callback_init,
            mock_response_unknown_objects):
        thread_callback = thread_callback_init
        message_callback = message_callback_init
        error_callback = error_callback_init
        completed_callback = completed_callback_init

        mock_web_factory = mocker.MagicMock()
        cancel_token = mocker.MagicMock()
        cancel_token.cancelled = False
        mock_disconnected = mocker.patch(
            "yellowdog_client.common.server_sent_events.sse4python.disconnected_state.DisconnectedState"
        )

        state = ConnectedState(url="URL", response=mock_response_unknown_objects, web_requester_factory=mock_web_factory)
        thread = state.run(
            message_received=message_callback,
            error_handle=error_callback,
            completed=completed_callback,
            cancel_token=cancel_token,
            continuation_callback=thread_callback
        )
        thread.join()

        assert self._callback_executed
        assert self._thread_result == mock_disconnected.return_value
        mock_disconnected.assert_called_once_with(
            url="URL", web_requester_factory=mock_web_factory
        )
        assert self._message_callback_executed
        assert len(self._message_callback_result) == 3
        for event in self._message_callback_result:
            assert type(event) == ServerSentEvent
            assert event.raw_data is None
            assert event.event_type is None
            assert event.last_event_id is None
            assert event.retry is None
        assert not self._error_callback_executed
        assert self._completed_callback_executed

    def test__run__non_cancelled__valid_events__expect_message_invoked_with_valid_values__complete_invoked__disconnect_returned__followed_by_callback(
            self, mocker, thread_callback_init, message_callback_init, error_callback_init, completed_callback_init,
            mock_response_full):
        thread_callback = thread_callback_init
        message_callback = message_callback_init
        error_callback = error_callback_init
        completed_callback = completed_callback_init

        mock_web_factory = mocker.MagicMock()
        cancel_token = mocker.MagicMock()
        cancel_token.cancelled = False
        mock_disconnected = mocker.patch(
            "yellowdog_client.common.server_sent_events.sse4python.disconnected_state.DisconnectedState"
        )

        state = ConnectedState(url="URL", response=mock_response_full, web_requester_factory=mock_web_factory)
        thread = state.run(
            message_received=message_callback,
            error_handle=error_callback,
            completed=completed_callback,
            cancel_token=cancel_token,
            continuation_callback=thread_callback
        )
        thread.join()

        assert self._callback_executed
        assert self._thread_result == mock_disconnected.return_value
        mock_disconnected.assert_called_once_with(
            url="URL", web_requester_factory=mock_web_factory
        )
        assert self._message_callback_executed
        assert len(self._message_callback_result) == 3
        index = 0
        for event in self._message_callback_result:
            index += 1
            assert type(event) == ServerSentEvent
            assert event.raw_data == "DATA%s" % str(index)
            assert event.event_type == "EVENT%s" % str(index)
            assert event.last_event_id == "ID%s" % str(index)
            assert event.retry == index

        assert not self._error_callback_executed
        assert self._completed_callback_executed
