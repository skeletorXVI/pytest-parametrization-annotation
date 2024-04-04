from dataclasses import dataclass
from typing import Any, Callable

_Default = object()
_DefaultCallable = lambda: None  # noqa: E731


@dataclass(slots=True, kw_only=True, frozen=True)
class Parametrized:
    indirect: bool = False
    default: Any = _Default
    default_factory: Callable[[], Any] = _DefaultCallable
