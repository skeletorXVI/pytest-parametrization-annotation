from typing import Annotated

import pytest
from pytest_parametrization_annotation import Parametrized


@pytest.fixture
def doubled(request):
    return request.param * 2


@pytest.mark.case("first", doubled=5, expected=10)
@pytest.mark.case("second", doubled=12, expected=24)
@pytest.mark.case("third", doubled=44, expected=88)
def test(
    doubled: Annotated[int, Parametrized(indirect=True)],
    expected: Annotated[int, Parametrized],
):
    assert doubled == expected
