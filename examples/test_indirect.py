from __future__ import annotations

from typing import Annotated, TYPE_CHECKING

import pytest
from pytest_parametrization_annotation import Parametrized

if TYPE_CHECKING:
    from _pytest.fixtures import FixtureRequest


@pytest.fixture
def doubled(request: FixtureRequest) -> int:
    value: int = request.param
    return value * 2


@pytest.mark.case(
    doubled=1,
    b=2,
    expected=4,
)
def test_addition(
    doubled: Annotated[int, Parametrized(indirect=True)],
    b: Annotated[int, Parametrized],
    expected: Annotated[int, Parametrized],
) -> None:
    assert doubled + b == expected
