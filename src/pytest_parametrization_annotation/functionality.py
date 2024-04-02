from typing import Annotated, Any, Callable, Mapping, get_origin, get_type_hints

from _pytest.python import Metafunc

from pytest_parametrization_annotation.annotation import (
    Parametrized,
    _Default,
    _DefaultCallable,
)
from pytest_parametrization_annotation.exceptions import ParameterValueUndefined


def get_parameters_from_type_hints(func: Callable) -> dict[str, Parametrized]:
    parameters = {}
    for name, type_hint in get_type_hints(func, include_extras=True).items():
        if get_origin(type_hint) is not Annotated:
            continue

        # Check if is annotated as a parameter
        try:
            parameter = next(
                annotation
                for annotation in type_hint.__metadata__
                if annotation is Parametrized or isinstance(annotation, Parametrized)
            )
        except StopIteration:
            continue

        parameters[name] = (
            parameter if isinstance(parameter, Parametrized) else Parametrized()
        )
    return parameters


def get_parametrized_value(
    kwargs: Mapping[str, Any], parameter: str, meta: Parametrized
) -> Any:
    if parameter in kwargs:
        return kwargs[parameter]
    if meta.default_factory is not _DefaultCallable:
        return meta.default_factory()
    if meta.default is not _Default:
        return meta.default
    raise KeyError(parameter)


def register_parametrized_cases(metafunc: Metafunc):
    function_definition = metafunc.definition
    markers = [mark for mark in function_definition.iter_markers(name="case")]
    if markers:
        func = getattr(function_definition.module, function_definition.name)
        parameters = get_parameters_from_type_hints(func)

        # Exit early if no parameters are annotated to be parametrized
        if not parameters:
            return

        cases = []
        ids = []
        for i, marker in enumerate(markers):
            case_id = marker.args[0] if len(marker.args) > 0 else None
            ids.append(case_id)

            try:
                cases.append(
                    tuple(
                        get_parametrized_value(marker.kwargs, parameter, meta)
                        for parameter, meta in parameters.items()
                    )
                )
            except KeyError as e:
                raise ParameterValueUndefined(
                    function_definition.nodeid,
                    case_id or i,
                    e.args[0],
                ) from e

        metafunc.parametrize(
            tuple(parameters),
            cases,
            indirect=[
                name for name, parameter in parameters.items() if parameter.indirect
            ],
            ids=ids,
        )