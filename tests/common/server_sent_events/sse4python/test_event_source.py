from yellowdog_client.common.server_sent_events.sse4python import EventSource
from yellowdog_client.common.server_sent_events.sse4python import EventSourceState
import pytest


class TestIsClosed(object):
    def test__token_source_cancelled__state_closed__expect_closed(self, mocker):
        mock_token = mocker.patch(
            "yellowdog_client.common.server_sent_events.sse4python.event_source.CancellationToken"
        )
        mock_token.return_value.cancelled = True
        state = mocker.MagicMock()
        state.state.return_value = EventSourceState.CLOSED

        source = EventSource(url=mocker.MagicMock(), factory=mocker.MagicMock())
        source.__setattr__("__current_state_internal", state)

        assert source.is_closed

    def test__token_source_non_cancelled__state_closed__expect_not_closed(self, mocker):
        mock_token = mocker.patch(
            "yellowdog_client.common.server_sent_events.sse4python.event_source.CancellationToken"
        )
        mock_token.return_value.cancelled = False
        state = mocker.MagicMock()
        state.state.return_value = EventSourceState.CLOSED

        source = EventSource(url=mocker.MagicMock(), factory=mocker.MagicMock())
        source.__setattr__("__current_state_internal", state)

        assert not source.is_closed

    def test__token_source_non_cancelled__state_not_closed__expect_closed(self, mocker):
        mock_token = mocker.patch(
            "yellowdog_client.common.server_sent_events.sse4python.event_source.CancellationToken"
        )
        mock_token.return_value.cancelled = True
        state = mocker.MagicMock()

        source = EventSource(url=mocker.MagicMock(), factory=mocker.MagicMock())
        source._current_state_internal = state

        state.state = EventSourceState.CONNECTING
        assert not source.is_closed
        state.state = EventSourceState.OPEN
        assert not source.is_closed


class TestSetCurrentState(object):
    def test__set_current_state__same_value__expect_no_dispatch(self, mocker):
        state = mocker.MagicMock()
        mock_on_status_change = mocker.patch("yellowdog_client.common.server_sent_events.sse4python.event_source.EventSource._on_status_changed")

        source = EventSource(url=mocker.MagicMock(), factory=mocker.MagicMock())
        # part of constructor
        mock_on_status_change.assert_called_once()

        source._current_state_internal = state
        source._current_state = state

        assert source._current_state_internal == state
        # still called once
        mock_on_status_change.assert_called_once()

    def test__set_current_state__expect_status_change_dispatch(self, mocker):
        state = mocker.MagicMock()
        state.state = "MY_CUSTOM_STATE"
        mock_on_status_change = mocker.patch("yellowdog_client.common.server_sent_events.sse4python.event_source.EventSource._on_status_changed")

        source = EventSource(url=mocker.MagicMock(), factory=mocker.MagicMock())
        source._current_state = state

        assert source._current_state_internal == state
        mock_on_status_change.assert_any_call(state="MY_CUSTOM_STATE")


class TestStart(object):
    def test__state_not_closed__expect_nothing_run(self, mocker):
        state = mocker.MagicMock()
        state.state = "RANDOM_STATE"
        mock_run = mocker.patch("yellowdog_client.common.server_sent_events.sse4python.event_source.EventSource._run")

        source = EventSource(url=mocker.MagicMock(), factory=mocker.MagicMock())
        original_token = source._token_source
        source._current_state = state

        source.start()

        assert source._token_source == original_token
        mock_run.assert_not_called()


class TestStart(object):
    def test__state_not_closed__expect_nothing_run(self, mocker):
        state = mocker.MagicMock()
        state.state = EventSourceState.OPEN
        mock_run = mocker.patch("yellowdog_client.common.server_sent_events.sse4python.event_source.EventSource._run")

        source = EventSource(url=mocker.MagicMock(), factory=mocker.MagicMock())
        original_token = source._token_source
        source._current_state = state

        source.start()

        assert source._token_source == original_token
        mock_run.assert_not_called()

    def test__state_closed__expect_run_called(self, mocker):
        state = mocker.MagicMock()
        state.state = EventSourceState.CLOSED
        mock_run = mocker.patch("yellowdog_client.common.server_sent_events.sse4python.event_source.EventSource._run")

        source = EventSource(url=mocker.MagicMock(), factory=mocker.MagicMock())
        original_token = source._token_source
        source._current_state = state

        source.start()

        assert source._token_source != original_token
        mock_run.assert_called_once()


class TestStop(object):
    def test__token_cancelled__expect_nothing_invoked(self, mocker):
        state = mocker.MagicMock()
        state.state = EventSourceState.OPEN
        mock_completed = mocker.patch("yellowdog_client.common.server_sent_events.sse4python.event_source.EventSource._on_event_source_completed")

        source = EventSource(url=mocker.MagicMock(), factory=mocker.MagicMock())
        source._token_source.cancel()

        source.stop()

        mock_completed.assert_not_called()

    def test__token_not_cancelled__expect_cancelled_and_complete_invoked(self, mocker):
        state = mocker.MagicMock()
        state.state = EventSourceState.OPEN
        mock_completed = mocker.patch("yellowdog_client.common.server_sent_events.sse4python.event_source.EventSource._on_event_source_completed")

        source = EventSource(url=mocker.MagicMock(), factory=mocker.MagicMock())

        assert not source._token_source.cancelled

        source.stop()

        assert source._token_source.cancelled
        mock_completed.assert_called_once()


class TestContinuationCallback(object):
    def test_token_cancelled__state_closed__expect_continuous_run_not_invoked(self, mocker):
        state = mocker.MagicMock()
        state.state = EventSourceState.CLOSED

        source = EventSource(url=mocker.MagicMock(), factory=mocker.MagicMock())
        source._token_source.cancel()

        source._continuation_callback(connection_state=state)

        state.run.assert_not_called()

    def test_token_not_cancelled__state_closed__expect_continuous_run_invoked(self, mocker):
        state = mocker.MagicMock()
        state.state = EventSourceState.CLOSED

        source = EventSource(url=mocker.MagicMock(), factory=mocker.MagicMock())
        assert not source._token_source.cancelled

        source._continuation_callback(connection_state=state)

        state.run.assert_called_once_with(
            message_received=source._on_event_received,
            error_handle=source._on_error_received,
            completed=source._on_event_source_completed,
            cancel_token=source._token_source,
            continuation_callback=source._continuation_callback
        )

    def test_token_cancelled__state_not_closed__expect_continuous_run_invoked(self, mocker):
        state = mocker.MagicMock()
        state.state = EventSourceState.CONNECTING

        source = EventSource(url=mocker.MagicMock(), factory=mocker.MagicMock())
        source._token_source.cancel()

        source._continuation_callback(connection_state=state)

        state.run.assert_called_once_with(
            message_received=source._on_event_received,
            error_handle=source._on_error_received,
            completed=source._on_event_source_completed,
            cancel_token=source._token_source,
            continuation_callback=source._continuation_callback
        )

    def test_token_not_cancelled__state_not_closed__expect_continuous_run_invoked(self, mocker):
        state = mocker.MagicMock()
        state.state = EventSourceState.CONNECTING

        source = EventSource(url=mocker.MagicMock(), factory=mocker.MagicMock())
        assert not source._token_source.cancelled

        source._continuation_callback(connection_state=state)

        state.run.assert_called_once_with(
            message_received=source._on_event_received,
            error_handle=source._on_error_received,
            completed=source._on_event_source_completed,
            cancel_token=source._token_source,
            continuation_callback=source._continuation_callback
        )


class TestOnStatusChanged(object):
    @pytest.fixture
    def result_fixture(self):
        self.__result = None
        return self.__result

    def set_result(self, state):
        self.__result = state

    def test__event_received(self, mocker, result_fixture):
        source = EventSource(url=mocker.MagicMock(), factory=mocker.MagicMock())

        source.bind(state_changed=self.set_result)

        thread = source._on_status_changed(state=EventSourceState.CONNECTING)
        thread.join()

        assert self.__result == EventSourceState.CONNECTING
