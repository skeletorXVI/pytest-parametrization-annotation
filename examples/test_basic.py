from typing import Annotated

import pytest
from pytest_parametrization_annotation import Parametrized


@pytest.mark.case(
    a=1,
    b=2,
    expected=3,
)
def test_addition(
    a: Annotated[int, Parametrized],
    b: Annotated[int, Parametrized],
    expected: Annotated[int, Parametrized],
) -> None:
    assert a + b == expected
