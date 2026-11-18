from typing import List

from yellowdog_client.common import CancellationToken


def test_runs_callbacks_once_when_cancelled():
    token = CancellationToken()
    calls: List[str] = []
    token.on_cancel(lambda: calls.append("first"))
    token.on_cancel(lambda: calls.append("second"))

    token.cancel()
    token.cancel()

    assert token.cancelled
    assert calls == ["first", "second"]


def test_runs_callback_immediately_when_already_cancelled():
    token = CancellationToken()
    token.cancel()
    calls: List[str] = []

    token.on_cancel(lambda: calls.append("late"))

    assert calls == ["late"]
