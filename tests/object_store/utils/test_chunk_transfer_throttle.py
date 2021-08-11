from yellowdog_client.object_store.utils import ChunkTransferThrottle
from cancel_token.cancel_token import CancellationToken


class TestChunkTransferThrottle(object):
    def test_constructor(self, mocker):
        mock_time = mocker.patch("yellowdog_client.object_store.utils.chunk_transfer_throttle.time")
        mock_time.time.return_value = 7

        throttle = ChunkTransferThrottle(throttle_period_sec=5)
        throttle.max_bytes_per_second = 80

        assert throttle._throttle_period_seconds == 5
        assert throttle._throttle_period_ms == 5000
        assert throttle._max_bytes_per_second == 80
        assert throttle._max_bytes_per_period == 80 * 5
        assert throttle._bytes_transferred == 0
        assert throttle._start_time == 7000
        assert throttle._end_time is None

    def test_start_and_end(self, mocker):
        mock_time = mocker.patch("yellowdog_client.object_store.utils.chunk_transfer_throttle.time")
        mock_time.time.return_value = 3

        throttle = ChunkTransferThrottle(throttle_period_sec=2)
        throttle.start()

        assert throttle._start_time == 3000
        assert throttle._end_time is None

        mock_time.time.return_value = 4

        throttle.stop()

        assert throttle._start_time == 3000
        assert throttle._end_time == 4000


class TestWait(object):
    def test__wait__no_max_bytes__expect_no_sleep(self, mocker):
        mock_time = mocker.patch("yellowdog_client.object_store.utils.chunk_transfer_throttle.time")
        token = CancellationToken()

        throttle = ChunkTransferThrottle(throttle_period_sec=2)
        throttle.max_bytes_per_second = 0

        throttle.wait_for_transfer_bandwidth(chunk_size=700, cancellation_token=token)

        mock_time.sleep.assert_not_called()

    def test__wait__max_bytes__token_is_cancelled__expect_no_sleep(self, mocker):
        mock_time = mocker.patch("yellowdog_client.object_store.utils.chunk_transfer_throttle.time")
        token = CancellationToken()
        token.cancel()

        throttle = ChunkTransferThrottle(throttle_period_sec=2)
        throttle.max_bytes_per_second = 800

        throttle.wait_for_transfer_bandwidth(chunk_size=700, cancellation_token=token)

        mock_time.sleep.assert_not_called()
        assert throttle._bytes_transferred == 0

    def test__wait__max_bytes__elapsed_time_exceeds_start_time__expect_no_sleep(self, mocker):
        mock_time = mocker.patch("yellowdog_client.object_store.utils.chunk_transfer_throttle.time")
        mock_time.time.side_effect = [1, 4]     # elapsed: 3000 ms
        token = CancellationToken()

        throttle = ChunkTransferThrottle(throttle_period_sec=2)     # throttle period: 2000 ms
        throttle.max_bytes_per_second = 800

        throttle.wait_for_transfer_bandwidth(chunk_size=700, cancellation_token=token)

        mock_time.sleep.assert_not_called()
        assert throttle._bytes_transferred == 700
        assert throttle._start_time == 4000

    def test__wait__max_bytes__chunk_size_does_not_reach_max_bytes_per_sec__expect_no_sleep(self, mocker):
        mock_time = mocker.patch("yellowdog_client.object_store.utils.chunk_transfer_throttle.time")
        mock_time.time.side_effect = [1, 2]
        token = CancellationToken()

        throttle = ChunkTransferThrottle(throttle_period_sec=2)
        throttle.max_bytes_per_second = 800
        throttle._bytes_transferred = 20

        throttle.wait_for_transfer_bandwidth(chunk_size=700, cancellation_token=token)

        mock_time.sleep.assert_not_called()
        assert throttle._bytes_transferred == 720
        assert throttle._start_time == 1000

    def test__wait__max_bytes__chunk_size_exceeds_max_bytes_per_sec__expect_sleep__second_call_exceeds_time__expect_exit(self, mocker):
        mock_time = mocker.patch("yellowdog_client.object_store.utils.chunk_transfer_throttle.time")
        mock_time.time.side_effect = [1, 3, 10]
        token = CancellationToken()

        throttle = ChunkTransferThrottle(throttle_period_sec=9)
        throttle.max_bytes_per_second = 800
        throttle._bytes_transferred = 300

        throttle.wait_for_transfer_bandwidth(chunk_size=700, cancellation_token=token)

        assert throttle._bytes_transferred == 700
        assert throttle._start_time == 10 * 1000
        mock_time.sleep.assert_called_once_with(7)


