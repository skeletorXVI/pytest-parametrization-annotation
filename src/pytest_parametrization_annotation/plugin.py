from __future__ import annotations

from pytest_parametrization_annotation.functionality import register_parametrized_cases
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from _pytest.python import Metafunc
    from _pytest.config import Config


def pytest_configure(config: Config) -> None:
    config.addinivalue_line(
        "markers", "case: Parametrize the test with the provided values."
    )


def pytest_generate_tests(metafunc: Metafunc) -> None:
    register_parametrized_cases(metafunc)
