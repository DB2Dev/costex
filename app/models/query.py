from pydantic import BaseModel, model_validator
from typing import List
from app.models.enums.queryOperation import QueryOperation
from app.models.table import Table
from app.models.condition import Condition
from app.models.column import Column
from app.models.enums.tableType import TableType
from app.models.enums.logicalOperator import LogicalOperator
from app.models.enums.algoChoice import AlgoChoice
from app.models.enums.indexType import IndexType


class Query(BaseModel):
    operation: QueryOperation
    table_name: TableType = None
    table: Table = None
    select_columns_names: List[str] = []
    select_columns: List[Column] = []
    filters: List[Condition] = None
    filters_operators: List[LogicalOperator] = []
    join_column_names: List[str] = []
    join_column: List[Column] = []
    join_table_name: TableType = None
    join_table: Table = None
    possible_join_algorithms: List[AlgoChoice] = []
    best_join_algorithm: AlgoChoice = None

    @model_validator(mode="before")
    def qval(cls, data):
        data["select_columns"] = []
        if data["operation"] == QueryOperation.SELECT:
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
            data["table"] = Table(name=data["table_name"])
            for column in data["table"].columns:
                if column.name in data["select_columns_names"]:
                    data["select_columns"].append(column)
            for filter in data["filters"]:
                if filter.column_name not in [
                    col.name for col in data["table"].columns
                ]:
                    raise ValueError("Filter column name is not valid")
                for column in data["table"].columns:
                    if column.name == filter.column_name:
                        filter.column = column

            if len(data["select_columns_names"]) != len(data["select_columns"]):
                raise ValueError(
                    "At least one of the select columns names are not valid"
                )

        elif data["operation"] == QueryOperation.JOIN:
            data["join_columns"] = []
            if data["select_columns_names"] is None:
                raise ValueError("Select columns cannot be empty")
            if data["table_name"] is None:
                raise ValueError("Table name cannot be empty")
            if len(data["join_column_names"]) < 1:
                raise ValueError("Join column name cannot be empty")
            if data["join_table_name"] is None:
                raise ValueError("Join table name cannot be empty")
            data["table"] = Table(name=data["table_name"])
            for column in data["table"].columns:
                if column.name in data["select_columns_names"]:
                    data["select_columns"].append(column)
            data["join_table"] = Table(name=data["join_table_name"])
            for column in data["join_table"].columns:
                if column.name in data["select_columns_names"]:
                    data["select_columns"].append(column)
            for column in data["table"].columns:
                if column.name == data["join_column_names"][0]:
                    data["join_columns"].append(column)
            if len(data["join_column_names"]) > 1:
                for column in data["join_table"].columns:
                    if column.name == data["join_column_names"][1]:
                        data["join_columns"].append(column)
            if len(data["join_columns"]) != len(data["join_column_names"]):
                raise ValueError("At least one of the join columns names are not valid")
            if len(data["select_columns_names"]) != len(data["select_columns"]):
                raise ValueError(
                    "At least one of the select columns names are not valid"
                )
        return data

    @model_validator(mode="after")
    def qval2(self):
        """
        assign possible execution plans/algorithms to
        filters and join algorithms to join
        """
        if self.operation == QueryOperation.SELECT:
            for filter in self.filters:
                possible_algorithms: List[AlgoChoice] = [AlgoChoice.FILE_SCAN]

                # if filter.condition_type == QueryType.EQUALITY:
                if filter.column.is_primary_key:
                    possible_algorithms.append(AlgoChoice.BINARY_SEARCH)
                    possible_algorithms.append(AlgoChoice.PRIMARY_INDEX)
                elif filter.column.has_index:
                    if (
                        filter.column.index_type == IndexType.CLUSTERED
                        and filter.column.is_unique
                    ):
                        possible_algorithms.append(AlgoChoice.BINARY_SEARCH)
                        possible_algorithms.append(AlgoChoice.CLUSTERED_INDEX)
                    elif filter.column.index_type == IndexType.SECONDARY:
                        possible_algorithms.append(AlgoChoice.SECONDARY_INDEX)
                # elif filter.condition_type == QueryType.RANGE:
                #     pass

                filter.possible_algorithms = possible_algorithms

        elif self.operation == QueryOperation.JOIN:
            possible_join_algorithms: List[AlgoChoice] = []

            self.possible_join_algorithms = possible_join_algorithms

        return self
