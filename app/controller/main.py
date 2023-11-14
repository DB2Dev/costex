import estimators.select as estimate_S
import estimators.join as estimate_J
from models.metadata.tables_info import TablesDetails
from models.query import Query
from models.enums.queryOperation import QueryOperation
from models.enums.algoChoice import AlgoChoice
from models.enums.queryType import QueryType
from typing import Dict, List, Tuple
from utils.cardinality import cardinality
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
                        sql.cost[AlgoChoice.FILE_SCAN] = estimate_S.file_scan(
                            TablesDetails.get_no_of_blocks(sql.table_name)
                        )

                    elif algo == AlgoChoice.BINARY_SEARCH:
                        if sql.filters[0].condition_type == QueryType.EQUALITY:
                            sql.cost[
                                AlgoChoice.BINARY_SEARCH
                            ] = estimate_S.binary_search_equal(
                                TablesDetails.get_no_of_blocks(sql.table_name)
                            )
                        else:
                            sql.cost[
                                AlgoChoice.BINARY_SEARCH
                            ] = estimate_S.binary_search_range(
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
                            ] = estimate_S.primary_index_equal()
                        else:
                            sql.cost[
                                AlgoChoice.PRIMARY_INDEX
                            ] = estimate_S.primary_index_range(
                                TablesDetails.get_no_of_blocks(sql.table_name),
                            )

                    elif algo == AlgoChoice.CLUSTERED_INDEX:
                        sql.cost[
                            AlgoChoice.CLUSTERED_INDEX
                        ] = estimate_S.clustering_index(
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
                            ] = estimate_S.secondary_index_equal(
                                cardinality(
                                    sql.filters[0].column,
                                    sql.table_name,
                                    sql.filters[0].condition_type,
                                ),
                            )
                        else:
                            sql.cost[
                                AlgoChoice.SECONDARY_INDEX
                            ] = estimate_S.secondary_index_range(
                                TablesDetails.get_no_of_records(sql.table_name)
                            )
            else:
                cardinalities: List[Tuple[int, float]] = []
                for index, condition in enumerate(sql.filters):
                    cardinalities.append(
                        (
                            index,
                            cardinality(
                                condition.column,
                                sql.table_name,
                                condition.condition_type,
                            ),
                        )
                    )
                cardinalities = sorted(cardinalities, key=lambda x: x[1])
                print(cardinalities)
                # 2. estimate_S the query cost
                for algo in sql.filters[cardinalities[0][0]].possible_algorithms:
                    print(sql.filters[cardinalities[0][0]].possible_algorithms)
                    if algo == AlgoChoice.FILE_SCAN:
                        sql.cost[AlgoChoice.FILE_SCAN] = estimate_S.file_scan(
                            TablesDetails.get_no_of_blocks(sql.table_name)
                        )

                    elif algo == AlgoChoice.BINARY_SEARCH:
                        if sql.filters[cardinalities[0][0]].condition_type == QueryType.EQUALITY:
                            sql.cost[
                                AlgoChoice.BINARY_SEARCH
                            ] = estimate_S.binary_search_equal(
                                TablesDetails.get_no_of_blocks(sql.table_name)
                            )
                        else:
                            sql.cost[
                                AlgoChoice.BINARY_SEARCH
                            ] = estimate_S.binary_search_range(
                                TablesDetails.get_no_of_blocks(sql.table_name),
                                TablesDetails.get_no_of_records(sql.table_name),
                                cardinality(
                                    sql.filters[cardinalities[0][0]].column,
                                    sql.table_name,
                                    QueryType.RANGE,
                                ),
                            )

                    elif algo == AlgoChoice.PRIMARY_INDEX:
                        if sql.filters[cardinalities[0][0]].condition_type == QueryType.EQUALITY:
                            sql.cost[
                                AlgoChoice.PRIMARY_INDEX
                            ] = estimate_S.primary_index_equal()
                        else:
                            sql.cost[
                                AlgoChoice.PRIMARY_INDEX
                            ] = estimate_S.primary_index_range(
                                TablesDetails.get_no_of_blocks(sql.table_name),
                            )

                    elif algo == AlgoChoice.CLUSTERED_INDEX:
                        sql.cost[
                            AlgoChoice.CLUSTERED_INDEX
                        ] = estimate_S.clustering_index(
                            cardinality(
                                sql.filters[cardinalities[0][0]].column,
                                sql.table_name,
                                sql.filters[cardinalities[0][0]].condition_type,
                            ),
                            TablesDetails.get_no_of_records(sql.table_name)
                            / TablesDetails.get_no_of_blocks(sql.table_name),
                        )

                    elif algo == AlgoChoice.SECONDARY_INDEX:
                        if sql.filters[cardinalities[0][0]].condition_type == QueryType.EQUALITY:
                            sql.cost[
                                AlgoChoice.SECONDARY_INDEX
                            ] = estimate_S.secondary_index_equal(
                                cardinality(
                                    sql.filters[cardinalities[0][0]].column,
                                    sql.table_name,
                                    sql.filters[cardinalities[0][0]].condition_type,
                                ),
                            )
                        else:
                            sql.cost[
                                AlgoChoice.SECONDARY_INDEX
                            ] = estimate_S.secondary_index_range(
                                TablesDetails.get_no_of_records(sql.table_name)
                            )
        elif sql.operation == QueryOperation.JOIN:
            sql.cost[AlgoChoice.NESTED_LOOP_JOIN] = estimate_J.nested_loop_join(
                sql.table_name, sql.join_table_name
            )
            sql.cost[
                AlgoChoice.INDEXED_NESTED_LOOP_JOIN
            ] = estimate_J.indexed_nested_loop_join(sql.table_name, sql.join_table_name, sql.join_columns[1])
            sql.cost[AlgoChoice.SORT_MERGE_JOIN] = estimate_J.sort_merge_join(
                sql.table_name, sql.join_table_name
            )


# Query = Query(
#     operation=QueryOperation.SELECT,
#     table_name=TableType.EMPLOYEE,
#     select_columns_names=["ssn", "middle_name"],
#     filters=[
#         Condition(
#             column_name="ssn",
#             operator=FilterOperator.BETWEEN,
#             condition_type=QueryType.RANGE,
#             values=["EM100000", "EM100010"],
#         ),
#         Condition(
#             column_name="middle_name",
#             operator=FilterOperator.GT,
#             condition_type=QueryType.RANGE,
#             values=["C"],
#         ),
#     ],
#     filters_operators=[LogicalOperator.AND],
# )

# pprint(Query.dict())
# pipeline(Query)
# pprint(Query.dict())

# Query = Query(
#     operation=QueryOperation.JOIN,
#     table_name=TableType.EMPLOYEE,
#     select_columns_names=["ssn", "project_name"],
#     join_column_names=["ssn", "mgr_ssn"],
#     join_table_name=TableType.PROJECT,
# )
