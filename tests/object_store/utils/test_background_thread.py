from yellowdog_client.object_store.utils import BackgroundThreadFactory
from yellowdog_client.object_store.utils import BackgroundThread


class TestBackgroundThreadFactory(object):
    def test(self):
        res = BackgroundThreadFactory().new_thread(target=TestBackgroundThreadFactory.test)
        
        assert type(res) == BackgroundThread


class TestBackgroundThread(object):
    def test__is_alive(self, mocker):
        mock_thread = mocker.patch("yellowdog_client.object_store.utils.background_thread.Thread")
        mock_thread.return_value.is_alive.return_value = True

        thread = BackgroundThread(target=TestBackgroundThread.test__is_alive)

        assert thread.is_alive() is True

    def target(self):
        self.target_executed = True

    def test_execute(self):
        res = BackgroundThreadFactory().new_thread(target=self.target)
        res.start()
        res.join()

        assert self.target_executed is True
