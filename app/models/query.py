from pydantic import BaseModel, model_validator
from typing import List
from app.models.enums.queryType import QueryType
from app.models.enums.queryOperation import QueryOperation
from app.models.table import Table
from app.models.condition import Condition
from app.models.column import Column
from app.models.enums.tableType import TableType
from app.models.enums.logicalOperator import LogicalOperator
from app.controller.algochooser import algo_chooser


class Query(BaseModel):
    operation: QueryOperation
    query_type: QueryType = None
    table_name: TableType = None
    table: Table = None
    select_columns_names: List[str] = None
    select_columns: List[Column] = None
    join_column_name: str = None
    join_column: Column = None
    join_table_name: TableType = None
    join_table: Table = None
    filters: List[Condition] = None
    filters_operators: List[LogicalOperator] = None

    # TODO: Add validation for the selected columns names/join column name
    # /and filter column names
    @model_validator(mode="before")
    def qval(cls, data):
        if data["operation"] == QueryOperation.SELECT:
            if data["query_type"] is None:
                raise ValueError("Query type cannot be empty")
            if data["select_columns_names"] is None:
                raise ValueError("Select columns cannot be empty")
            if data["table_name"] is None:
                raise ValueError("Table name cannot be empty")
            if data["filters"] is None:
                raise ValueError("Filters cannot be empty")
            if data["filters_operators"] is None:
                raise ValueError("Filters operators cannot be empty")
            if len(data["filters"]) != len(data["filters_operators"]) + 1:
                raise ValueError("Filters Operators not sufficient")
            data["table"] = Table(data["table_name"])
            for column in data["table"].columns:
                if column.name in data["select_columns_names"]:
                    data["select_columns"].append(column)
        elif data["operation"] == QueryOperation.JOIN:
            if data["select_columns_names"] is None:
                raise ValueError("Select columns cannot be empty")
            if data["table_name"] is None:
                raise ValueError("Table name cannot be empty")
            if data["join_column_name"] is None:
                raise ValueError("Join column name cannot be empty")
            if data["join_table_name"] is None:
                raise ValueError("Join table name cannot be empty")
            data["join_table"] = Table(data["join_table_name"])
            for column in data["join_table"].columns:
                if column.name == data["join_column_name"]:
                    data["join_column"] = column
        return data

    def __call__(self):
        return algo_chooser(self)
