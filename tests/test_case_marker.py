import os
from typing import Any, Mapping, Sequence

import pytest
from jinja2 import Environment, FileSystemLoader


@pytest.mark.parametrize(
    ("cases", "parameters", "fixtures"),
    [
        (
            [
                {
                    "has_id": True,
                    "id": "example",
                    "kwargs": {},
                },
            ],
            {},
            {},
        ),
        (
            [
                {
                    "has_id": False,
                    "id": None,
                    "kwargs": {},
                },
            ],
            {},
            {},
        ),
        (
            [
                {
                    "has_id": True,
                    "id": "example",
                    "kwargs": {},
                },
            ],
            {
                "example": {
                    "type": int,
                    "annotation": False,
                },
            },
            {
                "example": 5,
            },
        ),
        (
            [
                {
                    "has_id": False,
                    "id": None,
                    "kwargs": {},
                },
            ],
            {
                "example": {
                    "type": int,
                    "annotation": False,
                },
            },
            {
                "example": 5,
            },
        ),
        (
            [
                {
                    "has_id": True,
                    "id": "example",
                    "kwargs": {
                        "first": 1,
                    },
                },
            ],
            {
                "first": {
                    "type": int,
                    "annotation": "Parametrized()",
                },
            },
            {},
        ),
        (
            [
                {
                    "has_id": True,
                    "id": "example",
                    "kwargs": {
                        "first": 1,
                    },
                },
            ],
            {
                "first": {
                    "type": int,
                    "annotation": "Parametrized",
                },
            },
            {},
        ),
        (
            [
                {
                    "has_id": False,
                    "id": None,
                    "kwargs": {
                        "first": 1,
                    },
                },
            ],
            {
                "first": {
                    "type": int,
                    "annotation": "Parametrized()",
                },
            },
            {},
        ),
        (
            [
                {
                    "has_id": False,
                    "id": None,
                    "kwargs": {
                        "first": 1,
                    },
                },
            ],
            {
                "first": {
                    "type": int,
                    "annotation": "Parametrized",
                },
            },
            {},
        ),
        (
            [
                {
                    "has_id": True,
                    "id": "example",
                    "kwargs": {
                        "first": 1,
                        "second": False,
                    },
                },
            ],
            {
                "first": {
                    "type": int,
                    "annotation": "Parametrized()",
                },
                "second": {
                    "type": bool,
                    "annotation": "Parametrized()",
                },
            },
            {},
        ),
        (
            [
                {
                    "has_id": True,
                    "id": "example",
                    "kwargs": {
                        "first": 1,
                        "second": False,
                    },
                },
            ],
            {
                "first": {
                    "type": int,
                    "annotation": "Parametrized()",
                },
                "second": {
                    "type": bool,
                    "annotation": "Parametrized()",
                },
            },
            {},
        ),
        (
            [
                {
                    "has_id": False,
                    "id": None,
                    "kwargs": {
                        "first": 1,
                        "second": False,
                    },
                },
            ],
            {
                "first": {
                    "type": int,
                    "annotation": "Parametrized()",
                },
                "second": {
                    "type": bool,
                    "annotation": "Parametrized()",
                },
            },
            {},
        ),
        (
            [
                {
                    "has_id": False,
                    "id": None,
                    "kwargs": {
                        "first": 1,
                        "second": False,
                    },
                },
            ],
            {
                "first": {
                    "type": int,
                    "annotation": "Parametrized()",
                },
                "second": {
                    "type": bool,
                    "annotation": "Parametrized()",
                },
            },
            {},
        ),
        (
            [
                {
                    "has_id": False,
                    "id": None,
                    "kwargs": {
                        "first": "example string",
                        "second": False,
                    },
                },
            ],
            {
                "first": {
                    "type": str,
                    "annotation": "Parametrized",
                },
                "second": {
                    "type": bool,
                    "annotation": "Parametrized()",
                },
            },
            {},
        ),
        (
            [
                {
                    "has_id": False,
                    "id": None,
                    "kwargs": {
                        "first": "example string",
                        "second": False,
                    },
                },
            ],
            {
                "first": {
                    "type": str,
                    "annotation": "Parametrized",
                },
                "second": {
                    "type": bool,
                    "annotation": False,
                },
            },
            {"second": False},
        ),
        (
            [
                {
                    "has_id": True,
                    "id": "example",
                    "kwargs": {},
                },
            ],
            {
                "example": {
                    "type": int,
                    "annotation": "Parametrized(default=False)",
                },
            },
            {
                "example": 5,
            },
        ),
        (
            [
                {
                    "has_id": True,
                    "id": "example",
                    "kwargs": {},
                },
            ],
            {
                "example": {
                    "type": str,
                    "annotation": "Parametrized(default_factory=lambda: 'this is and example')",  # noqa: E501
                },
            },
            {},
        ),
    ],
)
def test_simple_parametrization(
    pytester,
    cases: Sequence[Mapping[str, Any]],
    parameters: Mapping[str, Any],
    fixtures: Mapping[str, Any],
):
    # Setup jinja engine to template
    env = Environment(
        loader=FileSystemLoader(
            os.path.join(os.path.dirname(os.path.realpath(__file__)), "templates")
        ),
    )
    template = env.get_template("test_case_marker/test_simple_parametrization.py.j2")
    python_code = template.render(cases=cases, parameters=parameters, fixtures=fixtures)

    pytester.makepyfile(python_code)

    result = pytester.runpytest()
    result.assert_outcomes(passed=len(cases))


@pytest.mark.parametrize(
    ["template", "expected_passed", "expected_failed"],
    [
        ("single_fixture", 1, 0),
        ("single_fixture_with_multiple_cases", 3, 0),
        ("multiple_fixture_with_multiple_cases", 3, 0),
        ("multiple_fixture_with_multiple_cases_with_failing_test", 3, 1),
    ],
)
def test_indirect_parametrization(
    pytester, template: str, expected_passed: int, expected_failed: int
):
    python_code = open(
        os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            f"templates/test_case_marker/{template}.py",
        )
    ).read()
    pytester.makepyfile(python_code)

    result = pytester.runpytest()
    result.assert_outcomes(passed=expected_passed, failed=expected_failed)


def test_missing_parameter(pytester):
    python_code = open(
        os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "templates/test_case_marker/missing_parameter.py",
        )
    ).read()
    pytester.makepyfile(python_code)

    result = pytester.runpytest()
    assert (
        "E   pytest_parametrization_annotation.exceptions.ParameterValueUndefined: test_missing_parameter.py::test | Case 'example': Failed to populate because the parameter 'second' is not provided and default is not configured." # noqa: E501
        in result.outlines
    )
    result.assert_outcomes(errors=1)
