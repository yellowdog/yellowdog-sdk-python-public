import pytest


class CallbackFixture(object):
    def callback(self, thread_result):
        self._callback_executed = True
        self._thread_result = thread_result

    @pytest.fixture
    def thread_callback_init(self):
        self._callback_executed = False
        self._thread_result = None
        return self.callback
