from typing import Dict, Callable, Any
# noinspection PyCompatibility
from concurrent.futures import Future
from threading import Lock


class SelfBindingStatusMatchPredicate(object):
    def __init__(self):
        self._when_status_matches_lock = Lock()         # type: Lock
        self._when_status_matches_predicates = {}       # type: Dict[Future, Callable[[Any], bool]]

    def _get_when_status_matches_futures(self):
        # type: () -> Dict[Future, Callable[[Any], bool]]
        return {
            x: self._when_status_matches_predicates[x]
            for x in self._when_status_matches_predicates
        }

    def _add_when_status_matches_future(self, future, predicate):
        # type: (Future, Callable[[Any], bool]) -> None
        self._when_status_matches_predicates[future] = predicate

    def _remove_when_status_matches_future(self, future):
        # type: (Future) -> None
        if future in self._when_status_matches_predicates:
            self._when_status_matches_predicates.pop(future)
