class ParameterValueUndefined(Exception):
    def __init__(
        self,
        test: str,
        case: int | str,
        parameter: str,
    ):
        self.test = test
        self.case = case
        self.parameter = parameter

    def __str__(self):
        return f"{self.test} | Case '{self.case}': Failed to populate because the parameter '{self.parameter}' is not provided and default is not configured."  # noqa: E501

    def __repr__(self):
        return f"Test -> {self.test} | Case -> {self.case} | Field -> {self.parameter}"