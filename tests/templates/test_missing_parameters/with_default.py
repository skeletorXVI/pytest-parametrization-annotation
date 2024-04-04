from typing import Annotated

import pytest
from pytest_parametrization_annotation import Parametrized


@pytest.mark.case("example")
def test(
    first: Annotated[int, Parametrized],
    second: Annotated[int, Parametrized(default=123)],
):
    assert first == 1
