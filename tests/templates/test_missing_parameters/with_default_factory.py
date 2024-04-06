from typing import Annotated

import pytest
from pytest_parametrization_annotation import Parametrized


@pytest.mark.case("example")
def test(
    first: Annotated[int, Parametrized(default_factory=lambda: 123)],
    second: Annotated[int, Parametrized],
):
    assert first == 1
