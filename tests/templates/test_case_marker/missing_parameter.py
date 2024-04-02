from typing import Annotated

import pytest
from pytest_parametrization_annotation import Parametrized


@pytest.mark.case("example", first=1)
def test(first: Annotated[int, Parametrized], second: Annotated[int, Parametrized]):
    assert first == second
