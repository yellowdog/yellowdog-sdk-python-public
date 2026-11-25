import re
import warnings
from dataclasses import dataclass, field
from typing import List

_TOKEN_CHARACTERS = r"!#$%&'*+\-.^_`|~0-9A-Za-z"

# A token, as defined in RFC 9110 section 5.6.2
_TOKEN = re.compile(f"[{_TOKEN_CHARACTERS}]+")
# Java's Character.isWhitespace characters, so a value is sent as the Java SDK sends it. Python's own whitespace also
# includes U+0085 and the non-breaking spaces U+00A0, U+2007 and U+202F.
_JAVA_WHITESPACE_CHARACTERS = (
    "\t\n\x0b\x0c\r\x1c\x1d\x1e\x1f \u1680\u2000\u2001\u2002\u2003\u2004\u2005\u2006\u2008\u2009\u200a"
    "\u2028\u2029\u205f\u3000"
)
_WHITESPACE = re.compile(f"[{_JAVA_WHITESPACE_CHARACTERS}]")
_CONTROL = re.compile(r"[\x00-\x1f\x7f-\x9f]")
_NOT_TOKEN_CHARACTER = re.compile(f"[^{_TOKEN_CHARACTERS}]")


@dataclass(frozen=True)
class Product:
    """
    Identifies an application in the User-Agent header that the SDK sends. The SDK adds it after its own version and
    the Python version, e.g. ``yd/1.1.0 yellowdog-sdk-python/16.4.0 python/3.12 my-app/1.2.0``.

    The name and version should each be a token, as defined in
    `RFC 9110 section 5.6.2 <https://www.rfc-editor.org/info/rfc9110/#section-5.6.2>`_. That is, one or more ASCII
    letters, digits or any of ``!#$%&'*+-.^_`|~``. If either isn't, a warning is issued and a token is sent in its
    place. Whitespace at either end is removed, and other whitespace becomes ``_``. A slash becomes ``#``. Other control
    characters are removed, and any other character that isn't allowed becomes ``_``. A name or version left empty is
    sent as ``unknown``.

    :param name: the application's name, such as its package name
    :param version: the application's version
    """

    name: str
    version: str

    def __post_init__(self) -> None:
        # The dataclass is frozen, so its fields can only be replaced through object.__setattr__
        object.__setattr__(self, "name", _sanitise("name", self.name))
        object.__setattr__(self, "version", _sanitise("version", self.version))


def _sanitise(component: str, value: str) -> str:
    if _TOKEN.fullmatch(value):
        return value

    sanitised = _WHITESPACE.sub("_", value.strip(_JAVA_WHITESPACE_CHARACTERS)).replace("/", "#")
    sanitised = _NOT_TOKEN_CHARACTER.sub("_", _CONTROL.sub("", sanitised))
    if not sanitised:
        sanitised = "unknown"

    # stacklevel 4 points the warning at the code that created the Product, past __post_init__ and __init__
    warnings.warn(
        f"Product {component} {value!r} is not an RFC 9110 token, so it is sent as {sanitised!r}",
        stacklevel=4
    )
    return sanitised


@dataclass
class UserAgent:
    application_id: str
    application_version: str
    python_version: str
    products: List[Product] = field(default_factory=list)
