from pydantic import BaseModel
from app.models.column import Column
from app.models.enums.filterOperator import FilterOperator
from app.models.enums.algoChoice import AlgoChoice
from typing import List


class Condition(BaseModel):
    column: Column
    operator: FilterOperator
    value: str | int | float
    possible_plans: List[AlgoChoice] = []
    best_plan: AlgoChoice = None
