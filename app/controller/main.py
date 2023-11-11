import app.estimators.select as estimate
from app.models.metadata.tables_info import TablesDetails
from app.models.query import Query
from app.models.enums.queryOperation import QueryOperation
from app.models.enums.filterOperator import FilterOperator
from app.models.enums.algoChoice import AlgoChoice
from app.models.enums.queryType import QueryType
from app.models.enums.tableType import TableType
from app.models.enums.logicalOperator import LogicalOperator
from app.models.condition import Condition
from typing import Dict, List, Tuple
from pprint import pprint

from app.utils.cardinality import cardinality
from .tokeniser import tokenise


def pipeline(sql: Query | str) -> Dict[AlgoChoice, int]:
    if isinstance(sql, str):
        sql = tokenise(sql)
        # replace tokenise in Query class as a static method
        # sql = Query.parse_raw(sql)

    if len(sql.cost) == 0:
        if sql.operation == QueryOperation.SELECT:
            if len(sql.filters) == 1:
                for algo in sql.filters[0].possible_algorithms:
                    if algo == AlgoChoice.FILE_SCAN:
                        sql.cost[AlgoChoice.FILE_SCAN] = estimate.file_scan(
                            TablesDetails.get_no_of_blocks(sql.table_name)
                        )

                    elif algo == AlgoChoice.BINARY_SEARCH:
                        if sql.filters[0].condition_type == QueryType.EQUALITY:
                            sql.cost[
                                AlgoChoice.BINARY_SEARCH
                            ] = estimate.binary_search_equal(
                                TablesDetails.get_no_of_blocks(sql.table_name)
                            )
                        else:
                            sql.cost[
                                AlgoChoice.BINARY_SEARCH
                            ] = estimate.binary_search_range(
                                TablesDetails.get_no_of_blocks(sql.table_name),
                                TablesDetails.get_no_of_records(sql.table_name),
                                cardinality(
                                    sql.filters[0].column,
                                    sql.table_name,
                                    QueryType.RANGE,
                                ),
                            )

                    elif algo == AlgoChoice.PRIMARY_INDEX:
                        if sql.filters[0].condition_type == QueryType.EQUALITY:
                            sql.cost[
                                AlgoChoice.PRIMARY_INDEX
                            ] = estimate.primary_index_equal()
                        else:
                            sql.cost[
                                AlgoChoice.PRIMARY_INDEX
                            ] = estimate.primary_index_range(
                                TablesDetails.get_no_of_blocks(sql.table_name),
                            )

                    elif algo == AlgoChoice.CLUSTERED_INDEX:
                        sql.cost[
                            AlgoChoice.CLUSTERED_INDEX
                        ] = estimate.clustering_index(
                            cardinality(
                                sql.filters[0].column,
                                sql.table_name,
                                sql.filters[0].condition_type,
                            ),
                            TablesDetails.get_no_of_records(sql.table_name)
                            / TablesDetails.get_no_of_blocks(sql.table_name),
                        )

                    elif algo == AlgoChoice.SECONDARY_INDEX:
                        if sql.filters[0].condition_type == QueryType.EQUALITY:
                            sql.cost[
                                AlgoChoice.SECONDARY_INDEX
                            ] = estimate.secondary_index_equal(
                                cardinality(
                                    sql.filters[0].column,
                                    sql.table_name,
                                    sql.filters[0].condition_type,
                                ),
                            )
                        else:
                            sql.cost[
                                AlgoChoice.SECONDARY_INDEX
                            ] = estimate.secondary_index_range(
                                TablesDetails.get_no_of_records(sql.table_name)
                            )
            else:
                cardinalities: List[Tuple[int, float]] = []
                for index, condition in enumerate(sql.filters):
                    cardinalities.append(
                        (
                            index,
                            cardinality(
                                condition.column_name,
                                sql.table_name,
                                condition.condition_type,
                            ),
                        )
                    )
                cardinalities = sorted(cardinalities, key=lambda x: x[1])
                # 2. estimate the query cost
                sql.filters[cardinalities[0][0]]
                pass
        elif sql.operation == QueryOperation.JOIN:
            # directly estimate the query cost
            pass


Query = Query(
    operation=QueryOperation.SELECT,
    table_name=TableType.EMPLOYEE,
    select_columns_names=["ssn", "middle_name"],
    filters=[
        Condition(
            column_name="ssn",
            operator=FilterOperator.BETWEEN,
            condition_type=QueryType.RANGE,
            values=["EM100000", "EM100010"],
        ),
        Condition(
            column_name="middle_name",
            operator=FilterOperator.GT,
            condition_type=QueryType.RANGE,
            values=["C"],
        ),
    ],
    filters_operators=[LogicalOperator.AND],
)


pprint(Query.dict())

# Query = Query(
#     operation=QueryOperation.JOIN,
#     table_name=TableType.EMPLOYEE,
#     select_columns_names=["ssn", "project_name"],
#     join_column_names=["ssn", "mgr_ssn"],
#     join_table_name=TableType.PROJECT,
# )
