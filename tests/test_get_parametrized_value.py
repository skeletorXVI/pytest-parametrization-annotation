from typing import Mapping, Any

import pytest

from pytest_parametrization_annotation import Parametrized
from pytest_parametrization_annotation.functionality import get_parametrized_value


@pytest.mark.parametrize(
    ("kwargs", "parameter", "meta", "expected"),
    [
        ({}, "first", Parametrized(default=5), 5),
        ({}, "first", Parametrized(default_factory=lambda: 6), 6),
        ({}, "first", Parametrized(default=5, default_factory=lambda: 6), 6),
        ({}, "second", Parametrized(default=5), 5),
        ({}, "second", Parametrized(default_factory=lambda: 6), 6),
        ({}, "second", Parametrized(default=5, default_factory=lambda: 6), 6),
        ({"first": 1, "second": 2}, "first", Parametrized(), 1),
        ({"first": 1, "second": 2}, "first", Parametrized(default=5), 1),
        (
            {"first": 1, "second": 2},
            "first",
            Parametrized(default_factory=lambda: 6),
            1,
        ),
        (
            {"first": 1, "second": 2},
            "first",
            Parametrized(default=5, default_factory=lambda: 6),
            1,
        ),
        ({"first": 1, "second": 2}, "second", Parametrized(), 2),
        ({"first": 1, "second": 2}, "second", Parametrized(default=5), 2),
        (
            {"first": 1, "second": 2},
            "second",
            Parametrized(default_factory=lambda: 6),
            2,
        ),
        (
            {"first": 1, "second": 2},
            "second",
            Parametrized(default=5, default_factory=lambda: 6),
            2,
        ),
        ({"third": 3, "fourth": 4}, "first", Parametrized(default=5), 5),
        (
            {"third": 3, "fourth": 4},
            "first",
            Parametrized(default_factory=lambda: 6),
            6,
        ),
        (
            {"third": 3, "fourth": 4},
            "first",
            Parametrized(default=5, default_factory=lambda: 6),
            6,
        ),
        ({"third": 3, "fourth": 4}, "second", Parametrized(default=5), 5),
        (
            {"third": 3, "fourth": 4},
            "second",
            Parametrized(default_factory=lambda: 6),
            6,
        ),
        (
            {"third": 3, "fourth": 4},
            "second",
            Parametrized(default=5, default_factory=lambda: 6),
            6,
        ),
    ],
    ids=(
        "empty kwargs | first | default",
        "empty kwargs | first | default factory",
        "empty kwargs | first | default and default factory",
        "empty kwargs | second | default",
        "empty kwargs | second | default factory",
        "empty kwargs | second | default and default factory",
        "matching kwargs | first | no default",
        "matching kwargs | first | default",
        "matching kwargs | first | default factory",
        "matching kwargs | first | default and default factory",
        "matching kwargs | second | no default",
        "matching kwargs | second | default",
        "matching kwargs | second | default factory",
        "matching kwargs | second | default and default factory",
        "non-matching kwargs | first | default",
        "non-matching kwargs | first | default factory",
        "non-matching kwargs | first | default and default factory",
        "non-matching kwargs | second | default",
        "non-matching kwargs | second | default factory",
        "non-matching kwargs | second | default and default factory",
    ),
)
def test_return(
    kwargs: Mapping[str, Any], parameter: str, meta: Parametrized, expected: Any
):
    actual = get_parametrized_value(kwargs, parameter, meta)
    assert actual == expected


@pytest.mark.parametrize(
    ("kwargs", "parameter", "meta"),
    [
        ({}, "first", Parametrized()),
        ({}, "second", Parametrized()),
        ({"third": 3, "fourth": 4}, "first", Parametrized()),
        ({"third": 3, "fourth": 4}, "second", Parametrized()),
    ],
    ids=(
        "empty kwargs | first | no default",
        "empty kwargs | second | no default",
        "non-matching kwargs | first | no default",
        "non-matching kwargs | second | no default",
    ),
)
def test_raises_key_error(
    kwargs: Mapping[str, Any], parameter: str, meta: Parametrized
):
    with pytest.raises(KeyError):
        get_parametrized_value({}, "first", Parametrized())
