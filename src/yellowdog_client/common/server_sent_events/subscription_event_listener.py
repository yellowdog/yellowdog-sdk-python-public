from typing import TypeVar, Generic

T = TypeVar('T')


class SubscriptionEventListener(Generic[T]):
    def updated(self, obj: TypeVar) -> None:
        """
        Invoked when an updated instance of the object is received from ``YellowDog Platform``.

        :param obj: an updated instance of the object for which the listener was registered
        """
        raise NotImplementedError("updated Needs implementation")

    def subscription_error(self, error: Exception) -> None:
        """
        Invoked if an error occurs on the subscription associated with this listener.

        :param error: the error that occurred
        """
        raise NotImplementedError("subscription_error Needs implementation")

    def subscription_cancelled(self) -> None:
        """
        Invoked if the server cancels the subscription associated with this listener
        """
        raise NotImplementedError("subscription_cancelled Needs implementation")
