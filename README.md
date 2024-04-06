# Package to use type annotations for parametrization in pytest

[![codecov](https://codecov.io/gh/skeletorXVI/pytest-parametrization-annotation/graph/badge.svg?token=22CXIHTW1Q)](https://codecov.io/gh/skeletorXVI/pytest-parametrization-annotation)
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>

This package allows the declaration of parametrization using type annotations and definition of test cases using a
decorator.

The primary reason of using this package over the standard `pytest.mark.parametrize` is readability and maintainability
of test cases especially if many test cases are defined for a single test function.
In addition, error messages are more informative compared to those provided by `pytest.mark.parametrize`.

## Install pytest-parametrization-annotation

```shell
pip install pytest-parametrization-annotation
```

## Usage

### Defining a test function parameter as parametrized

To define a parameter as parametrized, use the `Parametrized` class or an instance of the `Parametrized` class as an
annotation.

```python
from typing import Annotated
from pytest_parametrization_annotation import Parametrized


# Both definitions are treated the same
def test(a: Annotated[int, Parametrized], b: Annotated[int, Parametrized()]) -> None:
    ...
```

By default, parameters annotated in this way are treated as direct parameters.
To define a parameter as indirect, use the `indirect` argument when instantiating the `Parametrized` class.

```python
from typing import Annotated
from pytest_parametrization_annotation import Parametrized


def test(a: Annotated[int, Parametrized(indirect=True)]) -> None:
    ...
```

In addition, the `Parametrized` class provides to methods to define default values, `default` and `default_factory`.

```python
from typing import Annotated
from pytest_parametrization_annotation import Parametrized


def test(
    a: Annotated[int, Parametrized(default=1)],
    b: Annotated[str, Parametrized(default_factory=lambda: "Hello World!")]
) -> None:
    ...
```

## Defining test cases

To define test cases, use the `case` marker.
Each parametrized argument must be reflected as keyword in the case marker.

```python
from typing import Annotated
import pytest
from pytest_parametrization_annotation import Parametrized


@pytest.mark.case(a=1)
def test(a: Annotated[int, Parametrized]) -> None:
    ...
```

If a parametrized argument is missing from the case marker, the test suit will fail and a detailed error message will be provided.

```shell
examples/test_basic.py::test_addition | Case number 1: Failed to populate because the parameter 'b' is not provided and default is not configured.
```

Every case marker defines a single test case.
To define multiple test cases, use multiple case markers.

```python
from typing import Annotated
import pytest
from pytest_parametrization_annotation import Parametrized


@pytest.mark.case(a=1)
@pytest.mark.case(a=2)
@pytest.mark.case(a=3)
def test(a: Annotated[int, Parametrized]) -> None:
    ...
```


Optionally a case can be named by providing the first positional argument to the case marker.
If this is not provided the default pytest naming scheme is used.

```python
from typing import Annotated
import pytest
from pytest_parametrization_annotation import Parametrized


@pytest.mark.case("Example", a=1)
def test(a: Annotated[int, Parametrized]) -> None:
    ...
```

## Develop

### Install dependencies

```shell
poetry install
```

### Format code

```shell
poetry run ruff format
poetry run black .
```

### Run static type checker

```shell
poetry run mypy .
```

### Run tests

```shell
poetry run tox run-parallel
```
