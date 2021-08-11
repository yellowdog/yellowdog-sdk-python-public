from yellowdog_client.common import SynchronizedPredicatedRunner


class TestRun(object):
    def test__predicate_fails__expect_runnable_not_invoked(self, mocker):
        runnable = mocker.MagicMock()

        runner = SynchronizedPredicatedRunner(predicate=lambda: False)
        runner.run(runnable)

        runnable.assert_not_called()

    def test__predicate_passes__expect_runnable_invoked(self, mocker):
        runnable = mocker.MagicMock()

        runner = SynchronizedPredicatedRunner(predicate=lambda: True)
        runner.run(runnable)

        runnable.assert_called_once()
