import os

import pytest
from jinja2 import Environment, FileSystemLoader


@pytest.mark.parametrize(
    "filename, expected_errors",
    [
        ("test_with_default.py", [("named 'example'", "first")]),
        ("test_with_default_factory.py", [("named 'example'", "second")]),
    ],
)
def test_error_message_with_default(
    pytester,
    filename: str,
    expected_errors: list[tuple[str, str]],
) -> None:
    expected_error_messages = [
        f"test_error_message_with_default.py::test | Case {case}: Failed to populate because the parameter '{parameter}' is not provided and default is not configured."
        for case, parameter in expected_errors
    ]

    python_code = open(
        os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            f"templates/test_missing_parameters/{filename}",
        )
    ).read()
    pytester.makepyfile(python_code)

    result = pytester.runpytest()

    actual_error_messages = [
        line
        for line in result.outlines
        if "Failed to populate because the parameter" in line
    ]

    assert actual_error_messages == expected_error_messages

    result.assert_outcomes(errors=1)


@pytest.mark.parametrize(
    "cases, parameters, expected_errors",
    [
        (
            [
                {
                    "id": "example",
                    "parameters": [],
                },
            ],
            [
                "a",
            ],
            [
                ("named 'example'", "a"),
            ],
        ),
        (
            [
                {
                    "id": "example 1",
                    "parameters": [],
                },
                {
                    "id": "example 2",
                    "parameters": ["a"],
                },
                {
                    "id": "example 3",
                    "parameters": ["a"],
                },
            ],
            [
                "a",
            ],
            [
                ("named 'example 1'", "a"),
            ],
        ),
        (
            [
                {
                    "id": "example 1",
                    "parameters": [],
                },
                {
                    "id": "example 2",
                    "parameters": [],
                },
                {
                    "id": "example 3",
                    "parameters": ["a"],
                },
            ],
            [
                "a",
            ],
            [
                ("named 'example 1'", "a"),
                ("named 'example 2'", "a"),
            ],
        ),
        (
            [
                {
                    "id": "example 1",
                    "parameters": [],
                },
                {
                    "id": "example 2",
                    "parameters": [],
                },
                {
                    "id": "example 3",
                    "parameters": [],
                },
            ],
            [
                "a",
            ],
            [
                ("named 'example 1'", "a"),
                ("named 'example 2'", "a"),
                ("named 'example 3'", "a"),
            ],
        ),
        (
            [
                {
                    "id": "example 1",
                    "parameters": ["a"],
                },
                {
                    "id": "example 2",
                    "parameters": [],
                },
                {
                    "id": "example 3",
                    "parameters": [],
                },
            ],
            [
                "a",
            ],
            [
                ("named 'example 2'", "a"),
                ("named 'example 3'", "a"),
            ],
        ),
        (
            [
                {
                    "id": "example 1",
                    "parameters": ["a"],
                },
                {
                    "id": "example 2",
                    "parameters": ["a"],
                },
                {
                    "id": "example 3",
                    "parameters": [],
                },
            ],
            [
                "a",
            ],
            [
                ("named 'example 3'", "a"),
            ],
        ),
        (
            [
                {
                    "id": "example 1",
                    "parameters": ["a"],
                },
                {
                    "id": "example 2",
                    "parameters": [],
                },
                {
                    "id": "example 3",
                    "parameters": ["a"],
                },
            ],
            [
                "a",
            ],
            [
                ("named 'example 2'", "a"),
            ],
        ),
        (
            [
                {
                    "id": "example",
                    "parameters": ["a"],
                },
            ],
            [
                "a",
                "b",
            ],
            [
                ("named 'example'", "b"),
            ],
        ),
        (
            [
                {
                    "id": "example",
                    "parameters": ["b"],
                },
            ],
            [
                "a",
                "b",
            ],
            [
                ("named 'example'", "a"),
            ],
        ),
        (
            [
                {
                    "id": "example 1",
                    "parameters": ["a"],
                },
                {
                    "id": "example 2",
                    "parameters": ["a", "b"],
                },
                {
                    "id": "example 3",
                    "parameters": ["b"],
                },
            ],
            ["a", "b"],
            [
                ("named 'example 1'", "b"),
                ("named 'example 3'", "a"),
            ],
        ),
        (
            [{"id": None, "parameters": []}],
            ["a"],
            [("number 1", "a")],
        ),
        (
            [
                {
                    "id": None,
                    "parameters": ["a"],
                },
                {
                    "id": None,
                    "parameters": ["a"],
                },
                {
                    "id": None,
                    "parameters": [],
                },
            ],
            ["a"],
            [
                ("number 3", "a"),
            ],
        ),
        (
            [
                {
                    "id": None,
                    "parameters": ["a"],
                },
                {
                    "id": None,
                    "parameters": [],
                },
                {
                    "id": None,
                    "parameters": [],
                },
            ],
            ["a"],
            [
                ("number 2", "a"),
                ("number 3", "a"),
            ],
        ),
        (
            [
                {
                    "id": None,
                    "parameters": [],
                },
                {
                    "id": None,
                    "parameters": [],
                },
                {
                    "id": None,
                    "parameters": [],
                },
            ],
            ["a"],
            [
                ("number 1", "a"),
                ("number 2", "a"),
                ("number 3", "a"),
            ],
        ),
        (
            [
                {
                    "id": None,
                    "parameters": ["a"],
                },
                {
                    "id": "example",
                    "parameters": ["b"],
                },
            ],
            ["a", "b"],
            [
                ("number 1", "b"),
                ("named 'example'", "a"),
            ],
        ),
        (
            # This case verifies that not parametrized parameters are ignored
            [
                {
                    "id": None,
                    "parameters": ["b"],
                },
            ],
            ["a"],
            [
                ("number 1", "a"),
            ],
        ),
    ],
)
def test_error_message(
    pytester,
    cases: list[dict[str, str | None | list[str]]],
    parameters: list[str],
    expected_errors: list[tuple[str, str]],
) -> None:
    expected_error_messages = [
        f"test_error_message.py::test | Case {case}: Failed to populate because the parameter '{parameter}' is not provided and default is not configured."
        for case, parameter in expected_errors
    ]

    # Setup jinja engine to template
    env = Environment(
        loader=FileSystemLoader(
            os.path.join(os.path.dirname(os.path.realpath(__file__)), "templates")
        ),
    )
    template = env.get_template("test_missing_parameters/test_error_messages.py.j2")
    python_code = template.render(cases=cases, parameters=parameters)

    pytester.makepyfile(python_code)

    result = pytester.runpytest()

    actual_error_messages = [
        line
        for line in result.outlines
        if "Failed to populate because the parameter" in line
    ]

    assert actual_error_messages == expected_error_messages

    result.assert_outcomes(errors=1)
