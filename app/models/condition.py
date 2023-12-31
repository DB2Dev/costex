from pydantic import BaseModel, model_validator
from models.column import Column
from models.enums.filterOperator import FilterOperator
from models.enums.queryType import QueryType
from models.enums.algoChoice import AlgoChoice
from typing import List
from datetime import date


class Condition(BaseModel):
    column_name: str
    column: Column = None
    operator: FilterOperator
    condition_type: QueryType
    values: List[str | int | float | bool | date]
    possible_algorithms: List[AlgoChoice] = []
    best_algorithm: AlgoChoice = None

    @model_validator(mode="before")
    def validate_operator(cls, data):
        if data["operator"] == FilterOperator.BETWEEN:
            if len(data["values"]) != 2:
                raise ValueError(
                    "Value must be a list of two elements for BETWEEN operator"
                )
        else:
            if len(data["values"]) != 1:
                raise ValueError(
                    "Value must be a single element for the chosen operators"
                )
        if data["condition_type"] == QueryType.EQUALITY:
            if data["operator"] not in [FilterOperator.EQ]:
                raise ValueError("Operator not supported for the chosen condition type")
        elif data["condition_type"] == QueryType.RANGE:
            if data["operator"] == FilterOperator.EQ:
                raise ValueError("Operator not supported for the chosen condition type")

        return data
