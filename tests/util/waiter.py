import sys
from typing import Callable

import busypie


def is_debug() -> bool:
    gettrace = getattr(sys, 'gettrace', None)

    if gettrace is None:
        return False
    else:
        return gettrace()


def wait_until(predicate: Callable[[], bool], at_most=2) -> None:
    at_most = 1000 if is_debug() else at_most

    return busypie.wait().at_most(at_most, busypie.SECOND).until(predicate)
