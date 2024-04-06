from typing import Annotated, Callable, TypeVar, Generic

import pytest

from pytest_parametrization_annotation import Parametrized
from pytest_parametrization_annotation.functionality import (
    get_parameters_from_type_hints,
)


T = TypeVar("T")


class _Foo(Generic[T]):
    pass


def _no_parameters() -> None:
    pass


def _one_parameter(first: int) -> None:
    pass


def _one_generic_parameter(first: _Foo[int]) -> None:
    pass


def _one_builtin_generic_parameter(first: list[int]) -> None:
    pass


def _one_annotated_parameter(first: Annotated[int, "foo"]) -> None:
    pass


def _one_parametrized_parameter(first: Annotated[int, Parametrized]) -> None:
    pass


def _one_nested_annotated_parameter(first: Annotated[Annotated[int, "foo"], "foo"]) -> None:
    pass


def _one_annotated_nested_parametrized_parameter(
    first: Annotated[Annotated[int, Parametrized], "str"]
) -> None:
    pass


def _one_parametrized_annotated_parameter(
    first: Annotated[Annotated[int, "foo"], Parametrized]
) -> None:
    pass

def _one_parameter_one_annotated_parameter(
    first: int, second: Annotated[int, "foo"]
) -> None:
    pass


def _one_parameter_one_parametrized_parameter(
    first: int, second: Annotated[int, Parametrized]
) -> None:
    pass


def _one_annotated_parameter_one_parametrized_parameter(
    first: Annotated[int, "foo"], second: Annotated[int, Parametrized]
) -> None:
    pass


def _two_parametrized_parameters(
    first: Annotated[int, Parametrized], second: Annotated[int, Parametrized]
) -> None:
    pass


def _two_parametrized_parameters_one_annotated_parameter(
    first: Annotated[int, Parametrized],
    second: Annotated[int, Parametrized],
    third: Annotated[int, "foo"],
) -> None:
    pass


def _two_parametrized_parameters_one_generic_parameter(
    first: Annotated[int, Parametrized],
    second: _Foo[str],
    third: Annotated[int, Parametrized],
) -> None:
    pass


@pytest.mark.parametrize(
    ("func", "expected"),
    [
        (_no_parameters, {}),
        (_one_parameter, {}),
        (_one_generic_parameter, {}),
        (_one_builtin_generic_parameter, {}),
        (_one_annotated_parameter, {}),
        (_one_parametrized_parameter, {"first": Parametrized()}),
        (_one_nested_annotated_parameter, {}),
        (_one_annotated_nested_parametrized_parameter, {"first": Parametrized()}),
        (_one_parametrized_annotated_parameter, {"first": Parametrized()}),
        (_one_parameter_one_annotated_parameter, {}),
        (_one_parameter_one_parametrized_parameter, {"second": Parametrized()}),
        (_one_annotated_parameter_one_parametrized_parameter, {"second": Parametrized()}),
        (_two_parametrized_parameters, {"first": Parametrized(), "second": Parametrized()}),
        (
            _two_parametrized_parameters_one_annotated_parameter,
            {"first": Parametrized(), "second": Parametrized(),},
        ),
        (
            _two_parametrized_parameters_one_generic_parameter,
            {"first": Parametrized(),  "third": Parametrized()},
        ),
    ],
)
def test_return(func: Callable, expected: dict[str, Parametrized]) -> None:
    assert get_parameters_from_type_hints(func) == expected
