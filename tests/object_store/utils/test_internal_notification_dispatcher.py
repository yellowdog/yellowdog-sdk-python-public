from yellowdog_client.object_store.utils import InternalNotificationDispatcher
from yellowdog_client.object_store.utils import BackgroundThreadFactory


class TestInternalNotificationDispatcher(object):
    event_called = False
    event_args = None

    def handle_event(self, event_args):
        self.event_called = True
        self.event_args = event_args

    def test_dispatch__no_event_handler__expect_no_action_executed(self):
        dispatcher = InternalNotificationDispatcher(thread_factory=BackgroundThreadFactory())

        dispatcher.dispatch(event_handler=None, event_args="arguments")

        dispatcher.cancellation_token.cancel()
        assert self.event_called is False
        assert self.event_args is None

    def test_dispatch__token_is_cancelled__expect_no_action_invoked(self):
        dispatcher = InternalNotificationDispatcher(thread_factory=BackgroundThreadFactory())

        dispatcher.cancellation_token.cancel()

        dispatcher.dispatch(event_handler=self.handle_event, event_args="arguments")

        assert self.event_called is False
        assert self.event_args is None

    def test_dispatch__token_is_not_cancelled__expect_action_invoked_followed_with_thread_cancelled(self):
        dispatcher = InternalNotificationDispatcher(thread_factory=BackgroundThreadFactory())

        dispatcher.dispatch(event_handler=lambda event_args: dispatcher.cancellation_token.cancel() or self.handle_event(event_args), event_args="arguments")

        dispatcher.background_thread.join()

        assert self.event_called is True
        assert self.event_args == "arguments"



