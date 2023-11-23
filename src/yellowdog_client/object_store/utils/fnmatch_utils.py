import re
from typing import Optional

FN_MATCH_PATTERN: re.Pattern = re.compile(r'[?*!\[\]]')
FN_MATCH_PREFIX_PATTERN: re.Pattern = re.compile(r'^[^?*!\[\]]*/')


class FnmatchUtils:
    @staticmethod
    def uses_path_pattern(path: str) -> bool:
        return FN_MATCH_PATTERN.search(path) is not None

    @staticmethod
    def get_prefix_before_path_patterns(path: str) -> Optional[str]:
        match = FN_MATCH_PREFIX_PATTERN.search(path)
        if match is None:
            return None
        return match.group(0)
