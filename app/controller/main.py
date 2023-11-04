# from app.models.query import Query
# from app.models.enums.queryOperation import QueryOperation
# from app.models.enums.filterOperator import FilterOperator
# from app.models.enums.queryType import QueryType
# from app.models.enums.tableType import TableType
# from app.models.enums.logicalOperator import LogicalOperator
# from app.models.condition import Condition


def pipeline(sql):
    pass


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

# Query = Query(
#     operation=QueryOperation.JOIN,
#     table_name=TableType.EMPLOYEE,
#     select_columns_names=["ssn", "project_name"],
#     join_column_names=["ssn", "mgr_ssn"],
#     join_table_name=TableType.PROJECT,
# )
