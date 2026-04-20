from datetime import timedelta
from unittest.mock import patch, MagicMock

import pytest
from urllib3.util.retry import RequestHistory

from yellowdog_client.common.full_jitter_retry import FullJitterRetry


def test_new_preserves_params():

    # Given
    original = FullJitterRetry(
        total=3,
        retry_max_interval=timedelta(seconds=120),
        retry_initial_interval=timedelta(seconds=1),
    )

    # When
    cloned = original.new()

    # Then
    assert cloned.total == 3
    assert cloned.retry_max_interval == timedelta(seconds=120)
    assert cloned.retry_initial_interval == timedelta(seconds=1)


def test_new_allows_overriding():

    # Given
    original = FullJitterRetry(
        total=3,
        retry_max_interval=timedelta(seconds=120),
        retry_initial_interval=timedelta(seconds=1),
    )

    # When
    cloned = original.new(
        total=10,
        retry_max_interval=timedelta(seconds=240),
        retry_initial_interval=timedelta(seconds=2),
    )

    # Then
    assert cloned.total == 10
    assert cloned.retry_max_interval == timedelta(seconds=240)
    assert cloned.retry_initial_interval == timedelta(seconds=2)


def test_get_backoff_time_given_no_history_then_backoff_time_is_zero():

    retry = build_full_jitter_retry()
    backoff_time = retry.get_backoff_time()
    assert backoff_time == 0


def test_get_backoff_time_given_redirect_before_error_then_consecutive_errors_is_one():

    # Given
    retry = build_full_jitter_retry(retry_initial_interval=timedelta(seconds=1), retry_max_interval=timedelta(seconds=60))
    redirect = RequestHistory(method=None, url=None, error=None, status=None, redirect_location="http://example.com")
    error = RequestHistory(method=None, url=None, error=None, status=None, redirect_location=None)
    retry.history = (redirect, error)
    with patch("yellowdog_client.common.full_jitter_retry.random.random", return_value=1.0):

        # When
        backoff_time = retry.get_backoff_time()

        # Then
        #   max_sleep = timedelta(seconds=1) * ( 2 ** ( 1 - 1 )) = 1
        #   random = 1
        #   backoff_time = random * max_sleep = 1
        assert backoff_time == 1.0


# This assumes the retry_max_interval == 10s
backoff_error_count_to_time = [
    pytest.param(1, 1, id="1 errors"),
    pytest.param(2, 2, id="2 errors"),
    pytest.param(3, 4, id="3 errors"),
    pytest.param(4, 8, id="4 errors"),
    pytest.param(5, 10, id="5 errors (capped at 10seconds)"),
    pytest.param(6, 10, id="6 errors (capped at 10seconds)"),
]


@pytest.mark.parametrize("error_count,expected_backoff_time", backoff_error_count_to_time)
def test_get_backoff_time_without_jitter(error_count: int, expected_backoff_time: int):

    # Given
    retry = build_full_jitter_retry(retry_initial_interval=timedelta(seconds=1), retry_max_interval=timedelta(seconds=10))
    retry.history = build_history_of_errors(error_count)
    with patch("yellowdog_client.common.full_jitter_retry.random.random", return_value=1.0):

        # When
        backoff_time = retry.get_backoff_time()

        # Then
        assert backoff_time == expected_backoff_time


@pytest.mark.parametrize("error_count,expected_max_backoff_time", backoff_error_count_to_time)
def test_get_backoff_time(error_count: int, expected_max_backoff_time):

    # Given
    retry = build_full_jitter_retry(retry_initial_interval=timedelta(seconds=1), retry_max_interval=timedelta(seconds=10))
    retry.history = build_history_of_errors(error_count)

    # When
    backoff_time = retry.get_backoff_time()

    # Then
    assert backoff_time < expected_max_backoff_time
    assert backoff_time > 0


def test_get_backoff_time_given_retry_initial_interval_less_than_one_second():

    # Given
    retry_initial_interval = 0.5
    retry = build_full_jitter_retry(retry_initial_interval=timedelta(seconds=retry_initial_interval), retry_max_interval=timedelta(seconds=10))
    retry.history = build_history_of_errors(1)
    with patch("yellowdog_client.common.full_jitter_retry.random.random", return_value=1.0):

        # When
        backoff_time = retry.get_backoff_time()

        # Then
        assert backoff_time == retry_initial_interval


def test_get_backoff_time_given_retry_max_interval_less_than_one_second():

    # Given
    retry_max_interval = 0.75
    retry = build_full_jitter_retry(retry_initial_interval=timedelta(seconds=0.1), retry_max_interval=timedelta(seconds=retry_max_interval))
    retry.history = build_history_of_errors(100)
    with patch("yellowdog_client.common.full_jitter_retry.random.random", return_value=1.0):

        # When
        backoff_time = retry.get_backoff_time()

        # Then
        assert backoff_time == retry_max_interval


@patch.object(FullJitterRetry, 'get_backoff_time')
@patch("urllib3.util.retry.time.sleep")
def test_sleep_uses_get_backoff_time(sleep_mock: MagicMock, get_backoff_time: MagicMock):
    """This is to ensure that any changes to urllib3 do not result in get_backoff_time not being used"""

    # Given
    retry = build_full_jitter_retry()
    get_backoff_time.return_value = 0.01 # using a small value in case Retry sleeps a different way (the test would fail but would fail more slowly if this number were bigger)

    # When
    retry.sleep()

    # Then
    get_backoff_time.assert_called_once()
    sleep_mock.assert_called_once_with(0.01)


def build_full_jitter_retry(
        retry_count: int = 3,
        retry_max_interval: timedelta = timedelta(seconds=60),
        retry_initial_interval: timedelta = timedelta(seconds=1),
) -> FullJitterRetry:
    return FullJitterRetry(total=retry_count, retry_max_interval=retry_max_interval, retry_initial_interval=retry_initial_interval)


def build_history_of_errors(number_of_errors: int) -> tuple[RequestHistory, ...]:
    return tuple(
        RequestHistory(method=None, url=None, error=None, status=None, redirect_location=None)
            for _ in range(0, number_of_errors)
    )
