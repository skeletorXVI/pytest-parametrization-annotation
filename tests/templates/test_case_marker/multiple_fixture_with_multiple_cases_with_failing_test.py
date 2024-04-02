from typing import Annotated

import pytest
from pytest_parametrization_annotation import Parametrized


@pytest.fixture
def doubled(request):
    return request.param * 2


@pytest.fixture
def suffixed(request):
    return f"{request.param}_suffix"


@pytest.mark.case("first", doubled=5, suffixed="example", expected=10)
@pytest.mark.case("second", doubled=12, suffixed="abc", expected=24)
@pytest.mark.case("third", doubled=44, expected=88, suffixed="ddd")
@pytest.mark.case("fails", doubled=44, expected=99, suffixed="kkk")
def test(
    doubled: Annotated[int, Parametrized(indirect=True)],
    suffixed: Annotated[str, Parametrized(indirect=True)],
    expected: Annotated[int, Parametrized],
):
    assert doubled == expected
    assert suffixed[-7:] == "_suffix"
