from yellowdog_client.object_store.utils.external_notification_dispatcher import ExternalNotificationDispatcher


class TestDispatch(object):
    dispatched = False
    event_handler_invoked = False

    def dispatch_method(self, callback):
        self.dispatched = True
        callback()

    def raise_exception(self, event_args):
        self.event_handler_invoked = True
        raise Exception("Exception raised")

    def callback_invoke(self, event_args):
        self.event_handler_invoked = True
        self.event_args = event_args

    def test__no_event_handler__expect_nothing_dispatched(self):
        dispatcher = ExternalNotificationDispatcher(dispatch_method=self.dispatch_method)

        dispatcher.dispatch(event_handler=None, event_args="arguments")

        assert self.dispatched is False
        assert self.event_handler_invoked is False

    def test__event_handler_raises_exception__expect_dispatched_and_silent_fail(self):
        dispatcher = ExternalNotificationDispatcher(dispatch_method=self.dispatch_method)

        dispatcher.dispatch(event_handler=self.raise_exception, event_args="arguments")

        assert self.dispatched is True
        assert self.event_handler_invoked is True

    def test__event_handler_asserts__expect_dispatched(self):
        dispatcher = ExternalNotificationDispatcher(dispatch_method=self.dispatch_method)

        dispatcher.dispatch(event_handler=self.callback_invoke, event_args="arguments")

        assert self.dispatched is True
        assert self.event_handler_invoked is True
        assert self.event_args == "arguments"

