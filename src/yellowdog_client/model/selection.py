from dataclasses import dataclass
from typing import Generic, List, Optional, TypeVar

T = TypeVar('T')


@dataclass
class Selection(Generic[T]):
    """
    A selection of elements defined by an includes list, an excludes list, or both.

    The matching semantics are as follows:

      - **Include only** the selection matches any element that appears in :attr:`includes`.
      - **Exclude only** the selection matches any element that does *not* appear in :attr:`excludes`.
      - **Both specified** :attr:`includes` takes precedence; the effective set is the :attr:`includes` list with any elements also present in :attr:`excludes` removed. Only elements that survive this filtering are matched.
      - **Neither specified** both lists are empty; the selection matches nothing.
    """

    includes: Optional[List[T]] = None
    """
    Elements to include in the selection.

    When non-empty, only elements present in this list are candidates for matching (subject
    to further filtering by :attr:`excludes`).
    """

    excludes: Optional[List[T]] = None
    """
    Elements to exclude from the selection.

    When :attr:`includes` is empty, this list defines the set of elements that are
    *not* matched. When :attr:`includes` is non-empty, elements present in both lists
    are removed from the effective include set.
    """


# KEEP
def includes(includes: List[T]) -> Selection[T]:
    return Selection(includes=includes)

def excludes(excludes: List[T]) -> Selection[T]:
    return Selection(excludes=excludes)